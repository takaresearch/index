#!/usr/bin/env python3
"""
Import publications from BibTeX or RIS and (re)generate docs/research/achievements.md.

Design goals:
- No external dependencies (pure stdlib).
- Deterministic output (stable sorting).
- Dedupe by DOI when available; otherwise by normalized (title + year).

Usage:
  python scripts/import_achievements.py --input /path/to/export.bib --output docs/research/achievements.md
  python scripts/import_achievements.py --input /path/to/export.ris --output docs/research/achievements.md
"""

from __future__ import annotations

import argparse
import datetime as _dt
import os
import re
from dataclasses import dataclass
from typing import Iterable, List, Optional, Tuple


@dataclass(frozen=True)
class Pub:
    title: str
    year: Optional[int] = None
    authors: Tuple[str, ...] = ()
    venue: str = ""  # journal / booktitle
    volume: str = ""
    issue: str = ""
    pages: str = ""
    doi: str = ""
    url: str = ""
    kind: str = "article"  # article / inproceedings / preprint / other


_WS_RE = re.compile(r"\s+")
_PUNCT_RE = re.compile(r"[^0-9a-z]+")


def _norm(s: str) -> str:
    s = s.strip().lower()
    s = _WS_RE.sub(" ", s)
    s = _PUNCT_RE.sub(" ", s)
    return _WS_RE.sub(" ", s).strip()


def _clean_doi(s: str) -> str:
    s = s.strip()
    s = re.sub(r"^https?://(dx\.)?doi\.org/", "", s, flags=re.I)
    s = s.replace("DOI:", "").strip()
    return s


def _dedupe(pubs: Iterable[Pub]) -> List[Pub]:
    seen: set[str] = set()
    out: List[Pub] = []
    for p in pubs:
        doi_key = _clean_doi(p.doi) if p.doi else ""
        if doi_key:
            key = f"doi:{doi_key.lower()}"
        else:
            key = f"ty:{_norm(p.title)}|yr:{p.year or ''}"
        if key in seen:
            continue
        seen.add(key)
        out.append(p)
    return out


def _parse_ris(text: str) -> List[Pub]:
    # RIS is line-based: "TY  - JOUR", "TI  - Title", "AU  - Surname, Name", "PY  - 2021", "JO  - Journal", "VL  - 10", "IS  - 2", "SP  - 123", "EP  - 130", "DO  - 10....", "UR  - ...", "ER  -"
    entries: List[dict] = []
    cur: dict = {}
    for line in text.splitlines():
        if not line.strip():
            continue
        m = re.match(r"^([A-Z0-9]{2})\s*-\s*(.*)$", line)
        if not m:
            continue
        tag, val = m.group(1), m.group(2).strip()
        if tag == "TY":
            if cur:
                entries.append(cur)
            cur = {"TY": val, "AU": []}
        elif tag == "ER":
            if cur:
                entries.append(cur)
            cur = {}
        else:
            if tag == "AU":
                cur.setdefault("AU", []).append(val)
            else:
                # keep last by default; some fields may repeat (e.g., TI)
                cur[tag] = val
    if cur:
        entries.append(cur)

    pubs: List[Pub] = []
    for e in entries:
        title = e.get("TI") or e.get("T1") or ""
        if not title:
            continue
        year = None
        py = e.get("PY") or e.get("Y1") or ""
        m = re.search(r"\b(19|20)\d{2}\b", py)
        if m:
            year = int(m.group(0))
        venue = e.get("JO") or e.get("JF") or e.get("T2") or ""
        volume = e.get("VL", "")
        issue = e.get("IS", "")
        pages = ""
        sp, ep = e.get("SP", ""), e.get("EP", "")
        if sp and ep:
            pages = f"{sp}-{ep}"
        elif sp:
            pages = sp
        doi = _clean_doi(e.get("DO", ""))
        url = e.get("UR", "")
        ty = (e.get("TY", "") or "").upper()
        kind = "article" if ty in {"JOUR", "JFULL"} else "other"
        pubs.append(
            Pub(
                title=title.strip(),
                year=year,
                authors=tuple(a.strip() for a in e.get("AU", []) if a.strip()),
                venue=venue.strip(),
                volume=volume.strip(),
                issue=issue.strip(),
                pages=pages.strip(),
                doi=doi,
                url=url.strip(),
                kind=kind,
            )
        )
    return pubs


def _parse_bibtex(text: str) -> List[Pub]:
    # Minimal BibTeX parser for common exports. Not a full grammar.
    # Strategy: split entries by "@...{...," and then parse key = {value} / "value".
    pubs: List[Pub] = []
    # remove comments
    text = re.sub(r"(?m)^\s*%.*$", "", text)
    parts = re.split(r"(?=@\w+\s*[{(])", text)
    for part in parts:
        part = part.strip()
        if not part.startswith("@"):
            continue
        m = re.match(r"^@(\w+)\s*[{(]\s*([^,]+)\s*,", part, flags=re.S)
        if not m:
            continue
        entry_type = m.group(1).lower()
        body = part[m.end() :]
        body = re.sub(r"[})]\s*$", "", body.strip(), flags=re.S)

        fields: dict[str, str] = {}
        # field matcher: name = {...} or "..." or bareword
        # handle nested braces in a conservative way by scanning char-wise
        i = 0
        while i < len(body):
            # skip whitespace/commas
            while i < len(body) and body[i] in " \r\n\t,":
                i += 1
            if i >= len(body):
                break
            # read key
            j = i
            while j < len(body) and re.match(r"[A-Za-z0-9_:-]", body[j]):
                j += 1
            key = body[i:j].strip().lower()
            i = j
            # skip whitespace and '='
            while i < len(body) and body[i] in " \r\n\t=":
                i += 1
            if i >= len(body) or not key:
                break
            # read value
            if body[i] == "{":
                depth = 0
                start = i + 1
                i += 1
                while i < len(body):
                    if body[i] == "{":
                        depth += 1
                    elif body[i] == "}":
                        if depth == 0:
                            val = body[start:i]
                            i += 1
                            break
                        depth -= 1
                    i += 1
                else:
                    val = body[start:].strip()
            elif body[i] == '"':
                i += 1
                start = i
                while i < len(body) and body[i] != '"':
                    # naive; ignores escaped quotes
                    i += 1
                val = body[start:i]
                i += 1
            else:
                start = i
                while i < len(body) and body[i] not in ",\r\n":
                    i += 1
                val = body[start:i].strip()
            fields[key] = val.strip()

        title = fields.get("title", "").strip()
        if not title:
            continue
        year = None
        y = fields.get("year", "")
        if re.fullmatch(r"(19|20)\d{2}", y.strip()):
            year = int(y.strip())
        authors = tuple(a.strip() for a in re.split(r"\s+and\s+", fields.get("author", ""), flags=re.I) if a.strip())
        venue = fields.get("journal") or fields.get("booktitle") or ""
        volume = fields.get("volume", "")
        issue = fields.get("number", "") or fields.get("issue", "")
        pages = fields.get("pages", "")
        doi = _clean_doi(fields.get("doi", ""))
        url = fields.get("url", "") or fields.get("link", "")
        kind = "article" if entry_type in {"article"} else ("inproceedings" if entry_type in {"inproceedings", "conference"} else "other")
        pubs.append(
            Pub(
                title=_WS_RE.sub(" ", title).strip(),
                year=year,
                authors=authors,
                venue=_WS_RE.sub(" ", venue).strip(),
                volume=volume.strip(),
                issue=issue.strip(),
                pages=pages.strip(),
                doi=doi,
                url=url.strip(),
                kind=kind,
            )
        )
    return pubs


def _format_pub(p: Pub) -> str:
    # Markdown single bullet; keep compact.
    authors = ", ".join(p.authors) if p.authors else ""
    venue_parts = []
    if p.venue:
        venue_parts.append(f"*{p.venue}*")
    vol_issue = ""
    if p.volume and p.issue:
        vol_issue = f"{p.volume}({p.issue})"
    elif p.volume:
        vol_issue = p.volume
    elif p.issue:
        vol_issue = f"({p.issue})"
    if vol_issue:
        venue_parts.append(vol_issue)
    if p.pages:
        venue_parts.append(p.pages)
    if p.year:
        venue_parts.append(str(p.year))
    venue_line = ", ".join([v for v in venue_parts if v])
    doi_part = f" DOI: {p.doi}" if p.doi else ""
    url_part = f" [{p.url}]({p.url})" if (p.url and not p.doi) else ""

    # Prefer DOI link if present.
    if p.doi:
        doi_link = f"[{p.doi}](https://doi.org/{p.doi})"
        doi_part = f" DOI: {doi_link}"

    # Layout: Title — Authors — Venue — DOI/URL
    lines = [f"- **{p.title}**"]
    if authors:
        lines.append(f"  - {authors}")
    if venue_line:
        lines.append(f"  - {venue_line}{doi_part}{url_part}")
    else:
        tail = (doi_part or "").strip()
        if tail:
            lines.append(f"  - {tail.strip()}")
    return "\n".join(lines)


def _render_markdown(pubs: List[Pub], source_label: str) -> str:
    now = _dt.datetime.now().strftime("%Y-%m-%d")
    header = [
        "# 業績（公開）",
        "",
        "本ページは、公開可能な範囲での研究業績を記載する。",
        "",
        f"> 自動生成: `{now}`（入力: `{source_label}`）。重複は DOI 優先、次いで（題名＋年）の正規化で除去する。",
        "",
        "## 原著論文",
        "",
    ]

    # group by year desc, but keep as a single section for simplicity
    pubs_sorted = sorted(pubs, key=lambda p: (p.year or 0, _norm(p.title)), reverse=True)
    body = [_format_pub(p) for p in pubs_sorted if p.kind in {"article", "inproceedings", "other"}]
    if not body:
        body = ["- （未登録）"]
    return "\n".join(header + body + [""])


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="Path to BibTeX (.bib) or RIS (.ris) file")
    ap.add_argument("--output", required=True, help="Output markdown path (e.g., docs/research/achievements.md)")
    args = ap.parse_args()

    in_path = args.input
    out_path = args.output
    if not os.path.exists(in_path):
        raise SystemExit(f"Input not found: {in_path}")
    with open(in_path, "r", encoding="utf-8", errors="replace") as f:
        text = f.read()

    ext = os.path.splitext(in_path)[1].lower()
    if ext in {".ris"}:
        pubs = _parse_ris(text)
    elif ext in {".bib", ".bibtex"}:
        pubs = _parse_bibtex(text)
    else:
        raise SystemExit("Unsupported input. Use .bib or .ris")

    pubs = _dedupe(pubs)
    md = _render_markdown(pubs, os.path.basename(in_path))
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"Wrote {len(pubs)} unique items to {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


