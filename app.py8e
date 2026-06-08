import os
import io
import uuid
from flask import Flask, request, send_file, redirect, url_for, render_template

# ==========================================
# 1. PATH RESOLUTION LAYER (FORCES UI DETECTION)
# ==========================================
# This explicitly tells Flask exactly where your templates/ folder is located on Vercel
base_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(base_dir, 'templates')
static_dir = os.path.join(base_dir, 'static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
application = app  # Explicit WSGI reference for Vercel's backend builder

# ==========================================
# 2. DOCUMENT RENDERING ENGINE IMPORTS
# ==========================================
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor

from docx import Document
from docx.shared import Inches, Pt, RGBColor

# ==========================================
# 3. VERIFIED STATELESS ARCHITECTURE DATA
# ==========================================
MOCK_USER_PAYLOAD = {
    "name": "Applicant Core",
    "optimized_cv": "=== PROFESSIONAL EXPERIENCE ===\n- Managed high-end server configurations across infrastructure lines.\n- Handled enterprise operational targets smoothly.\n=== CORE EXPERTISE MATRIX ===\n- Project Scaling\n- Financial Risk Allocation Control"
}

# ==========================================
# 4. HIGH-FIDELITY LAYOUT COMPILERS
# ==========================================
def generate_styled_pdf(style_type, name, content_dict):
    pdf_buffer = io.BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    
    styles = getSampleStyleSheet()
    primary_color = HexColor("#1e3a8a") if style_type == "professional" else HexColor("#065f46") if style_type == "modern" else HexColor("#000000")
    accent_color = HexColor("#0284c7") if style_type == "professional" else HexColor("#10b981") if style_type == "modern" else HexColor("#555555")

    title_style = ParagraphStyle('CVTitle', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=24, leading=28, textColor=primary_color, spaceAfter=4)
    subtitle_style = ParagraphStyle('CVSubtitle', parent=styles['Normal'], fontName='Helvetica', fontSize=10, leading=14, textColor=accent_color, spaceAfter=12)
    heading_style = ParagraphStyle('CVHeading', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=14, leading=18, textColor=primary_color, spaceBefore=14, spaceAfter=6)
    body_style = ParagraphStyle('CVBody', parent=styles['Normal'], fontName='Helvetica', fontSize=10, leading=14, textColor=HexColor("#334155"), spaceAfter=6)

    story = [
        Paragraph(name.upper(), title_style),
        Paragraph("Verified Strategic Application Profile | Operational Stream Deliverable", subtitle_style),
        HRFlowable(width="100%", thickness=1.5, color=primary_color, spaceBefore=1, spaceAfter=15)
    ]

    sections = content_dict.get("optimized_cv", "").split("===")
    for section in sections:
        if not section.strip():
            continue
        lines = section.strip().split("\n")
        section_title = lines[0].replace("===", "").strip()
        
        story.append(Paragraph(section_title, heading_style))
        story.append(HRFlowable(width="30%", thickness=1, color=accent_color, hAlign='LEFT', spaceBefore=1, spaceAfter=8))
        
        body_text = "\n".join(lines[1:])
        for paragraph_line in body_text.split("\n"):
            if paragraph_line.strip():
                if paragraph_line.strip().startswith("-") or paragraph_line.strip().startswith("•"):
                    clean_line = "• " + paragraph_line.strip().lstrip("- •")
                    story.append(Paragraph(clean_line, ParagraphStyle('CVBullet', parent=body_style, leftIndent=12, firstLineIndent=-8)))
                else:
                    story.append(Paragraph(paragraph_line.strip(), body_style))
                    
    doc.build(story)
    pdf_buffer.seek(0)
    return pdf_buffer.getvalue()

def generate_styled_docx(style_type, name, content_dict):
    doc = Document()
    for s in doc.sections:
        s.top_margin = Inches(0.5)
        s.bottom_margin = Inches(0.5)
        s.left_margin = Inches(0.5)
        s.right_margin = Inches(0.5)

    title = doc.add_paragraph()
    run = title.add_run(name.upper())
    run.font.name = 'Arial'
    run.font.size = Pt(24)
    run.font.bold = True
    run.font.color.rgb = RGBColor(30, 58, 138) if style_type == "professional" else RGBColor(6, 95, 70) if style_type == "modern" else RGBColor(0,0,0)

    cv_sections = content_dict.get("optimized_cv", "").split("===")
    for section in cv_sections:
        if not section.strip():
            continue
        lines = section.strip().split("\n")
        section_title = lines[0].replace("===", "").strip()
        
        h = doc.add_paragraph()
        hrun = h.add_run(section_title)
        hrun.font.name = 'Arial'
        hrun.font.size = Pt(14)
        hrun.font.bold = True
        hrun.font.color.rgb = run.font.color.rgb
        
        body_text = "\n".join(lines[1:])
        for line in body_text.split("\n"):
            if line.strip():
                p = doc.add_paragraph()
                if line.strip().startswith("-") or line.strip().startswith("•"):
                    p.paragraph_format.left_indent = Inches(0.25)
                    prun = p.add_run("• " + line.strip().lstrip("- •"))
                else:
                    prun = p.add_run(line.strip())
                prun.font.name = 'Arial'
                prun.font.size = Pt(10)
                
    out = io.BytesIO()
    doc.save(out)
    out.seek(0)
    return out.getvalue()

# ==========================================
# 5. PRODUCTION ROUTING INFRASTRUCTURE
# ==========================================
@app.route('/')
def home_dashboard():
    return redirect(url_for('customer_dashboard'))

@app.route('/dashboard/customer')
def customer_dashboard():
    # Renders the HTML frontend sheet utilizing the absolute container paths
    return render_template('dashboard_customer.html', user=MOCK_USER_PAYLOAD)

@app.route('/api/download/<fmt>')
def download_compiled_file(fmt):
    style_selection = request.args.get("style", "professional")
    if fmt == "pdf":
        pdf_bytes = generate_styled_pdf(style_selection, MOCK_USER_PAYLOAD.get("name"), MOCK_USER_PAYLOAD)
        return send_file(io.BytesIO(pdf_bytes), mimetype='application/pdf', as_attachment=True, download_name=f'Stormcore_{style_selection}.pdf')
    elif fmt == "docx":
        docx_bytes = generate_styled_docx(style_selection, MOCK_USER_PAYLOAD.get("name"), MOCK_USER_PAYLOAD)
        return send_file(io.BytesIO(docx_bytes), mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document', as_attachment=True, download_name=f'Stormcore_{style_selection}.docx')
    return redirect(url_for('customer_dashboard'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
