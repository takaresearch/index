#!/usr/bin/env python3
"""
HTML to PDF converter with Japanese support using reportlab
"""

import sys
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from html.parser import HTMLParser
import re

class HTMLTextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []
        self.current_tag = None
        
    def handle_data(self, data):
        self.text.append(data)
        
    def get_text(self):
        return ''.join(self.text)

def extract_text_from_html(html_file):
    """Extract text content from HTML file"""
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Remove HTML tags and extract text
    text = re.sub(r'<[^>]+>', '', html_content)
    # Clean up whitespace
    text = re.sub(r'\s+', ' ', text)
    return text

def html_to_pdf(html_file, pdf_file, font_size=10, margin=0.5):
    """Convert HTML file to PDF with Japanese support"""
    
    # Try to register Japanese fonts (common Windows fonts)
    japanese_fonts = [
        ('YuGothic', 'Yu Gothic'),
        ('Meiryo', 'Meiryo'),
        ('MSGothic', 'MS Gothic'),
    ]
    
    # Use default font if Japanese fonts are not available
    font_name = 'Helvetica'
    
    # Create PDF document
    doc = SimpleDocTemplate(
        pdf_file,
        pagesize=A4,
        rightMargin=margin*inch,
        leftMargin=margin*inch,
        topMargin=margin*inch,
        bottomMargin=margin*inch
    )
    
    # Create styles
    styles = getSampleStyleSheet()
    
    # Custom styles with smaller font
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=font_size,
        leading=font_size * 1.4,
        fontName=font_name,
        alignment=TA_LEFT,
        spaceAfter=4,
    )
    
    heading1_style = ParagraphStyle(
        'CustomHeading1',
        parent=styles['Heading1'],
        fontSize=font_size + 6,
        leading=(font_size + 6) * 1.2,
        fontName=font_name,
        spaceAfter=8,
        spaceBefore=12,
    )
    
    heading2_style = ParagraphStyle(
        'CustomHeading2',
        parent=styles['Heading2'],
        fontSize=font_size + 4,
        leading=(font_size + 4) * 1.2,
        fontName=font_name,
        spaceAfter=6,
        spaceBefore=10,
    )
    
    heading3_style = ParagraphStyle(
        'CustomHeading3',
        parent=styles['Heading3'],
        fontSize=font_size + 2,
        leading=(font_size + 2) * 1.2,
        fontName=font_name,
        spaceAfter=4,
        spaceBefore=8,
    )
    
    # Read HTML and extract text
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Parse HTML and build story
    story = []
    
    # Simple HTML parsing - extract headings and paragraphs
    lines = html_content.split('\n')
    current_paragraph = []
    
    for line in lines:
        line = line.strip()
        if not line:
            if current_paragraph:
                text = ' '.join(current_paragraph)
                story.append(Paragraph(text, normal_style))
                story.append(Spacer(1, 4))
                current_paragraph = []
            continue
            
        # Check for headings
        if line.startswith('<h1'):
            if current_paragraph:
                text = ' '.join(current_paragraph)
                story.append(Paragraph(text, normal_style))
                story.append(Spacer(1, 4))
                current_paragraph = []
            # Extract heading text
            match = re.search(r'<h1[^>]*>(.*?)</h1>', line, re.DOTALL)
            if match:
                heading_text = re.sub(r'<[^>]+>', '', match.group(1)).strip()
                story.append(Paragraph(heading_text, heading1_style))
                story.append(Spacer(1, 8))
        elif line.startswith('<h2'):
            if current_paragraph:
                text = ' '.join(current_paragraph)
                story.append(Paragraph(text, normal_style))
                story.append(Spacer(1, 4))
                current_paragraph = []
            match = re.search(r'<h2[^>]*>(.*?)</h2>', line, re.DOTALL)
            if match:
                heading_text = re.sub(r'<[^>]+>', '', match.group(1)).strip()
                story.append(Paragraph(heading_text, heading2_style))
                story.append(Spacer(1, 6))
        elif line.startswith('<h3'):
            if current_paragraph:
                text = ' '.join(current_paragraph)
                story.append(Paragraph(text, normal_style))
                story.append(Spacer(1, 4))
                current_paragraph = []
            match = re.search(r'<h3[^>]*>(.*?)</h3>', line, re.DOTALL)
            if match:
                heading_text = re.sub(r'<[^>]+>', '', match.group(1)).strip()
                story.append(Paragraph(heading_text, heading3_style))
                story.append(Spacer(1, 4))
        elif line.startswith('<p') or line.startswith('<li'):
            # Extract paragraph/list item text
            match = re.search(r'<[^>]+>(.*?)</[^>]+>', line, re.DOTALL)
            if match:
                text = re.sub(r'<[^>]+>', '', match.group(1)).strip()
                if text:
                    current_paragraph.append(text)
        elif line.startswith('<hr'):
            if current_paragraph:
                text = ' '.join(current_paragraph)
                story.append(Paragraph(text, normal_style))
                story.append(Spacer(1, 4))
                current_paragraph = []
            story.append(Spacer(1, 8))
    
    # Add remaining paragraph
    if current_paragraph:
        text = ' '.join(current_paragraph)
        story.append(Paragraph(text, normal_style))
    
    # Build PDF
    doc.build(story)
    print(f"PDF created successfully: {pdf_file}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python html_to_pdf.py <html_file> [output_pdf] [font_size] [margin]")
        sys.exit(1)
    
    html_file = sys.argv[1]
    
    if not os.path.exists(html_file):
        print(f"Error: File not found: {html_file}")
        sys.exit(1)
    
    # Determine output PDF filename
    if len(sys.argv) >= 3:
        pdf_file = sys.argv[2]
    else:
        pdf_file = os.path.splitext(html_file)[0] + '.pdf'
    
    # Get font size and margin from arguments or use defaults
    font_size = int(sys.argv[3]) if len(sys.argv) >= 4 else 10
    margin = float(sys.argv[4]) if len(sys.argv) >= 5 else 0.5
    
    html_to_pdf(html_file, pdf_file, font_size, margin)
