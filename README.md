# 足部・足関節外科ノート（GitHub Pages）

本リポジトリは、足部・足関節外科に関する記録を **Markdownで執筆** し、GitHub Pages に **自動公開** するための最小構成である。  
公開するのは教育的・一般化可能な内容に限定し、症例同定性のある情報や、執筆中原稿は公開対象から厳密に除外する。

## 構成

- `docs/`: 公開サイト（GitHub Pagesに掲載されるMarkdown）
  - `index.md`: Landing
  - `clinical/`: 臨床
  - `research/`: 研究（公開可能な内容のみ）
- `mkdocs.yml`: サイト設定
- `.github/workflows/deploy-pages.yml`: push時にPagesへデプロイ
- `private/`（**非公開**）: 執筆中の原稿・メモ（`.gitignore`で追跡除外）

## ローカル執筆（Cursor想定）

### 1) セットアップ

```bash
cd "/Users/takah/Library/CloudStorage/Dropbox/[整形外科ノート]orto_note/ts_foot_and_ankle_github/index"
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2) プレビュー

```bash
mkdocs serve
```

ブラウザで `http://127.0.0.1:8000/` を開き、Markdownを保存するたびに反映される。

## GitHub Pages 公開（初回だけの設定）

1. GitHub上で本リポジトリの **Settings → Pages** を開く  
2. **Build and deployment** を **GitHub Actions** に設定する  
3. `main` ブランチへ push すると、自動で公開される

## 研究「執筆中」を非公開にする原則

### 推奨運用（最小労力・最大安全側）

- 執筆中の原稿は **必ず** `private/` に置く（例: `private/manuscripts/`, `private/notes/`）
- `private/` は `.gitignore` により **git追跡されない**（= 公開リポジトリに載らない）

## 業績（Achievements）の一括更新（重複除去つき）

ResearchGate等から文献情報を **BibTeX（.bib）または RIS（.ris）** でエクスポートできる場合、下記のスクリプトで `docs/research/achievements.md` を自動生成できる。

1. エクスポートファイルを `private/` に保存する（例: `private/achievements.bib`）
2. 生成を実行する

```bash
cd "/Users/takah/Library/CloudStorage/Dropbox/[整形外科ノート]orto_note/ts_foot_and_ankle_github/index"
python scripts/import_achievements.py --input private/achievements.bib --output docs/research/achievements.md
```

重複は **DOI優先**、次いで **（題名＋年）の正規化**で除去する。

### 重要

`private/` の中身は、意図せず `git add -f` 等で追跡対象にしない限り公開されない。  
一方で、機微情報（未匿名化データ等）の取り扱いは、所属施設の規程と情報セキュリティ方針に従うこと。


