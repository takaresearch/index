#!/usr/bin/env python3
"""
Markdown to PDF converter with Japanese support
Converts markdown file to PDF with 10pt font and narrow margins
"""

import sys
import os
import markdown
from weasyprint import HTML, CSS
from pathlib import Path

def markdown_to_pdf(md_file, pdf_file, font_size='10pt', margin='0.5in'):
    """Convert markdown file to PDF with custom styling"""
    
    # Read markdown file
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Convert markdown to HTML
    html_content = markdown.markdown(
        md_content,
        extensions=['extra', 'tables', 'fenced_code', 'toc']
    )
    
    # Create full HTML document with CSS styling
    html_doc = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        @page {{
            size: A4;
            margin: {margin};
            font-size: {font_size};
        }}
        body {{
            font-family: "Yu Gothic", "Meiryo", "MS Gothic", "Hiragino Sans", sans-serif;
            font-size: {font_size};
            line-height: 1.4;
            color: #000;
        }}
        h1 {{
            font-size: 16pt;
            font-weight: bold;
            margin-top: 12pt;
            margin-bottom: 8pt;
            page-break-after: avoid;
        }}
        h2 {{
            font-size: 14pt;
            font-weight: bold;
            margin-top: 10pt;
            margin-bottom: 6pt;
            page-break-after: avoid;
        }}
        h3 {{
            font-size: 12pt;
            font-weight: bold;
            margin-top: 8pt;
            margin-bottom: 4pt;
            page-break-after: avoid;
        }}
        p {{
            margin: 4pt 0;
            text-align: justify;
        }}
        ul, ol {{
            margin: 4pt 0;
            padding-left: 20pt;
        }}
        li {{
            margin: 2pt 0;
        }}
        code {{
            font-family: "Courier New", monospace;
            font-size: 9pt;
            background-color: #f5f5f5;
            padding: 1pt 2pt;
        }}
        pre {{
            font-family: "Courier New", monospace;
            font-size: 9pt;
            background-color: #f5f5f5;
            padding: 4pt;
            margin: 4pt 0;
            overflow: auto;
            page-break-inside: avoid;
        }}
        blockquote {{
            margin: 4pt 0;
            padding-left: 10pt;
            border-left: 2pt solid #ccc;
        }}
        hr {{
            margin: 8pt 0;
            border: none;
            border-top: 1pt solid #ccc;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 4pt 0;
            font-size: 9pt;
        }}
        th, td {{
            border: 1pt solid #ccc;
            padding: 2pt 4pt;
        }}
        th {{
            background-color: #f0f0f0;
            font-weight: bold;
        }}
    </style>
</head>
<body>
{html_content}
</body>
</html>"""
    
    # Convert HTML to PDF
    HTML(string=html_doc).write_pdf(pdf_file)
    print(f"PDF created successfully: {pdf_file}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python md_to_pdf.py <markdown_file> [output_pdf] [font_size] [margin]")
        sys.exit(1)
    
    md_file = sys.argv[1]
    
    if not os.path.exists(md_file):
        print(f"Error: File not found: {md_file}")
        sys.exit(1)
    
    # Determine output PDF filename
    if len(sys.argv) >= 3:
        pdf_file = sys.argv[2]
    else:
        pdf_file = os.path.splitext(md_file)[0] + '.pdf'
    
    # Get font size and margin from arguments or use defaults
    font_size = sys.argv[3] if len(sys.argv) >= 4 else '10pt'
    margin = sys.argv[4] if len(sys.argv) >= 5 else '0.5in'
    
    markdown_to_pdf(md_file, pdf_file, font_size, margin)
