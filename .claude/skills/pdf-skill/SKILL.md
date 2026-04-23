---
name: pdf-skill
description: |
  Generate styled PDF documents from markdown text, reports, or structured data.
  Use when user asks to create, export, or save content as a PDF file.
  Handles headings, paragraphs, bold/italic, lists, tables, code blocks, and horizontal rules.
---

# PDF Generation Skill

Convert markdown content to a branded, styled PDF. Upload it and return the CDN URL as a `file` artifact.

## Dependencies

Install once per session if not already available:

```bash
pip install reportlab
```

No other packages required — the generator uses only `reportlab` with a built-in markdown parser.

## Workflow

1. **Collect content** — gather the full text from the conversation or ask the user to provide it. Content may be markdown, a report draft, data tables, or plain prose.

2. **Write markdown to temp file** — use a descriptive kebab-case filename:
   ```
   /tmp/<content-slug>.md
   ```

3. **Write the generator script** to `/tmp/gen_pdf.py` using the template below.

4. **Generate the PDF**:
   ```bash
   python3 /tmp/gen_pdf.py /tmp/<slug>.md /tmp/<slug>.pdf "<Document Title>"
   ```

5. **Upload**:
   ```bash
   higgsfieldcli upload-file --file /tmp/<slug>.pdf
   ```

6. **Return** the CDN URL as a `file` artifact:
   ```json
   {"type": "file", "id": "<cdn_url>", "preview": "<cdn_url>", "label": "<Title>.pdf"}
   ```

## Generator Script — write to `/tmp/gen_pdf.py`

```python
#!/usr/bin/env python3
"""Markdown → styled PDF via ReportLab (no HTML intermediate, no extra deps)."""
import re
import sys
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    HRFlowable,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

W, H = A4

# Brand palette (matches Higgsfield UI tokens)
BRAND   = colors.HexColor('#4FCEE4')
DARK    = colors.HexColor('#1A1C1F')
MUTED   = colors.HexColor('#898A8B')
LIGHT   = colors.HexColor('#F0F0F0')
SUCCESS = colors.HexColor('#53C546')
ERROR   = colors.HexColor('#E72930')


def _styles():
    base = getSampleStyleSheet()
    return {
        'title': ParagraphStyle('pdftitle', fontName='Helvetica-Bold', fontSize=26,
                                 textColor=BRAND, spaceAfter=4*mm, leading=32),
        'h1':    ParagraphStyle('h1', fontName='Helvetica-Bold', fontSize=20,
                                 textColor=DARK, spaceBefore=8*mm, spaceAfter=3*mm, leading=26),
        'h2':    ParagraphStyle('h2', fontName='Helvetica-Bold', fontSize=15,
                                 textColor=DARK, spaceBefore=6*mm, spaceAfter=2*mm, leading=20),
        'h3':    ParagraphStyle('h3', fontName='Helvetica-BoldOblique', fontSize=12,
                                 textColor=DARK, spaceBefore=4*mm, spaceAfter=2*mm, leading=16),
        'body':  ParagraphStyle('body', fontName='Helvetica', fontSize=10,
                                 textColor=DARK, leading=15, spaceAfter=3*mm,
                                 alignment=TA_JUSTIFY),
        'bullet':ParagraphStyle('bullet', fontName='Helvetica', fontSize=10,
                                 textColor=DARK, leading=15, leftIndent=8*mm,
                                 spaceAfter=1.5*mm),
        'num':   ParagraphStyle('num', fontName='Helvetica', fontSize=10,
                                 textColor=DARK, leading=15, leftIndent=8*mm,
                                 spaceAfter=1.5*mm),
        'code':  ParagraphStyle('code', fontName='Courier', fontSize=9,
                                 textColor=DARK, backColor=LIGHT,
                                 leftIndent=4*mm, rightIndent=4*mm,
                                 spaceAfter=3*mm, leading=13),
        'th':    ParagraphStyle('th', fontName='Helvetica-Bold', fontSize=9,
                                 textColor=DARK, leading=13),
        'td':    ParagraphStyle('td', fontName='Helvetica', fontSize=9,
                                 textColor=DARK, leading=13),
    }


def _inline(text: str) -> str:
    """Convert inline markdown to ReportLab XML markup (safe escaping first)."""
    # XML-safe
    text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    # Bold
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'__(.+?)__',     r'<b>\1</b>', text)
    # Italic
    text = re.sub(r'\*(.+?)\*', r'<i>\1</i>', text)
    text = re.sub(r'_(.+?)_',   r'<i>\1</i>', text)
    # Inline code
    text = re.sub(r'`(.+?)`', r'<font name="Courier">\1</font>', text)
    return text


def _parse_table(lines: list[str], styles: dict) -> Table:
    """Parse a GFM table block into a ReportLab Table."""
    rows = []
    for line in lines:
        # skip separator row (--|-- pattern)
        if re.match(r'^[\s|:\-]+$', line):
            continue
        cells = [c.strip() for c in line.strip('|').split('|')]
        rows.append(cells)

    if not rows:
        return None

    style = styles['th'] if True else styles['td']
    col_count = max(len(r) for r in rows)
    available_w = W - 50 * mm
    col_w = available_w / col_count

    formatted = []
    for i, row in enumerate(rows):
        s = styles['th'] if i == 0 else styles['td']
        formatted.append([Paragraph(_inline(c), s) for c in row])

    t = Table(formatted, colWidths=[col_w] * col_count, repeatRows=1)
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0, 0), (-1,  0), LIGHT),
        ('FONTNAME',      (0, 0), (-1,  0), 'Helvetica-Bold'),
        ('FONTSIZE',      (0, 0), (-1, -1), 9),
        ('GRID',          (0, 0), (-1, -1), 0.25, MUTED),
        ('TOPPADDING',    (0, 0), (-1, -1), 2 * mm),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2 * mm),
        ('LEFTPADDING',   (0, 0), (-1, -1), 2 * mm),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 2 * mm),
        ('ROWBACKGROUNDS',(0, 1), (-1, -1), [colors.white, LIGHT]),
        ('VALIGN',        (0, 0), (-1, -1), 'TOP'),
    ]))
    return t


def _build_story(md_text: str, title: str, styles: dict) -> list:
    story: list = []

    # Title block
    story.append(Paragraph(title, styles['title']))
    story.append(HRFlowable(width='100%', thickness=1.5, color=BRAND, spaceAfter=6 * mm))

    lines = md_text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]

        # --- Fenced code block ---
        if line.strip().startswith('```'):
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('```'):
                code_lines.append(lines[i])
                i += 1
            story.append(Preformatted('\n'.join(code_lines), styles['code']))
            i += 1
            continue

        # --- Table block ---
        # Detect by presence of | in line and next line being separator
        if '|' in line and i + 1 < len(lines) and re.match(r'^[\s|:\-]+$', lines[i + 1]):
            table_lines = []
            while i < len(lines) and '|' in lines[i]:
                table_lines.append(lines[i])
                i += 1
            t = _parse_table(table_lines, styles)
            if t:
                story.append(t)
                story.append(Spacer(1, 3 * mm))
            continue

        # --- Headings ---
        m = re.match(r'^(#{1,3})\s+(.*)', line)
        if m:
            level = len(m.group(1))
            text = _inline(m.group(2))
            style_key = f'h{level}'
            story.append(Paragraph(text, styles.get(style_key, styles['h3'])))
            i += 1
            continue

        # --- Horizontal rule ---
        if re.match(r'^(\-{3,}|_{3,}|\*{3,})$', line.strip()):
            story.append(HRFlowable(width='100%', thickness=0.5, color=MUTED, spaceAfter=3 * mm))
            i += 1
            continue

        # --- Unordered list item ---
        m = re.match(r'^[\-\*\+]\s+(.*)', line)
        if m:
            story.append(Paragraph(f'• {_inline(m.group(1))}', styles['bullet']))
            i += 1
            continue

        # --- Ordered list item ---
        m = re.match(r'^\d+\.\s+(.*)', line)
        if m:
            num_match = re.match(r'^(\d+)\.\s+', line)
            n = num_match.group(1) if num_match else '1'
            story.append(Paragraph(f'{n}. {_inline(m.group(1))}', styles['num']))
            i += 1
            continue

        # --- Blank line (paragraph break) ---
        if not line.strip():
            story.append(Spacer(1, 2 * mm))
            i += 1
            continue

        # --- Regular paragraph / continuation ---
        para_lines = [line]
        i += 1
        while i < len(lines) and lines[i].strip() and not re.match(
            r'^(#{1,3}\s|[\-\*\+]\s|\d+\.\s|```|---$|___$|\*\*\*$)', lines[i]
        ) and '|' not in lines[i]:
            para_lines.append(lines[i])
            i += 1
        text = ' '.join(para_lines)
        story.append(Paragraph(_inline(text), styles['body']))

    return story


def build_pdf(md_path: str, pdf_path: str, title: str = 'Document') -> None:
    md_text = Path(md_path).read_text(encoding='utf-8')
    styles = _styles()
    story = _build_story(md_text, title, styles)

    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        leftMargin=25 * mm,
        rightMargin=25 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm,
        title=title,
        author='Higgsfield',
    )
    doc.build(story)
    print(f'PDF written: {pdf_path}')


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: gen_pdf.py <input.md> <output.pdf> [Title]')
        sys.exit(1)
    build_pdf(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else 'Document')
```

## Naming Convention

| Item | Pattern | Example |
|------|---------|---------|
| Markdown source | `/tmp/<slug>.md` | `/tmp/skincare-report.md` |
| PDF output | `/tmp/<slug>.pdf` | `/tmp/skincare-report.pdf` |
| Artifact label | Human title + `.pdf` | `Skincare Trend Report.pdf` |

## Supported Markdown

| Element | Syntax |
|---------|--------|
| Headings | `# H1`, `## H2`, `### H3` |
| Bold | `**text**` or `__text__` |
| Italic | `*text*` or `_text_` |
| Inline code | `` `code` `` |
| Fenced code block | ```` ``` ```` ... ```` ``` ```` |
| Bullet list | `- item` / `* item` |
| Numbered list | `1. item` |
| Table | GFM pipe table with `---` separator |
| Horizontal rule | `---` |
| Paragraph | Any non-special block of text |

## Error Handling

If `reportlab` is missing: run `pip install reportlab` first.

If generation fails with a parse error: simplify the markdown (remove unsupported HTML tags, nested lists, or images) and retry.

If the PDF is blank: check that `/tmp/<slug>.md` was written correctly before running the script.
