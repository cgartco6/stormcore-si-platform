# Add these structural layout models to the top of your app.py file
from reportlab.lib.colors import HexColor
from reportlab.platypus import Table, TableStyle, HRFlowable
from reportlab.lib import colors

def generate_styled_pdf(style_type, name, content_dict):
    """
    Sovereign PDF Engine: Generates highly tailored, professional layout visual structures
    Styles available: 'professional' (Corporate Navy), 'modern' (Slate & Emerald Accent), 'traditional' (Classic Minimalist)
    """
    pdf_buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        pdf_buffer, 
        pagesize=letter, 
        rightMargin=36, 
        leftMargin=36, 
        topMargin=36, 
        bottomMargin=36
    )
    
    styles = getSampleStyleSheet()
    
    # 2026 Structural Color Matrices
    primary_color = HexColor("#0f172a")    # Slate Dark Default
    accent_color = HexColor("#475569")     # Cool Muted Gray
    
    if style_type == "professional":
        primary_color = HexColor("#1e3a8a")  # Deep Corporate Navy
        accent_color = HexColor("#0284c7")   # Executive Sky Blue
    elif style_type == "modern":
        primary_color = HexColor("#065f46")  # Deep Emerald
        accent_color = HexColor("#10b981")   # Vibrant Mint Border
    elif style_type == "traditional":
        primary_color = HexColor("#000000")  # Pure Timeless Black
        accent_color = HexColor("#555555")   # Charcoal Gray Neutral

    # Custom Style Parameter Injections
    title_style = ParagraphStyle('CVTitle', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=24, leading=28, textColor=primary_color, spaceAfter=4)
    subtitle_style = ParagraphStyle('CVSubtitle', parent=styles['Normal'], fontName='Helvetica', fontSize=10, leading=14, textColor=accent_color, spaceAfter=12)
    heading_style = ParagraphStyle('CVHeading', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=14, leading=18, textColor=primary_color, spaceBefore=14, spaceAfter=6)
    body_style = ParagraphStyle('CVBody', parent=styles['Normal'], fontName='Helvetica', fontSize=10, leading=14, textColor=HexColor("#334155"), spaceAfter=6)

    story = []

    # Header Panel Construction Array
    story.append(Paragraph(name.upper(), title_style))
    story.append(Paragraph("Verified Strategic Application Matrix Profile | Operational Stream Deliverable", subtitle_style))
    
    # Visual Separator Line Element
    story.append(HRFlowable(width="100%", thickness=1.5, color=primary_color, spaceBefore=1, spaceAfter=15))

    # Parse and structuralize block sections out of the raw text strings safely
    sections = content_dict.get("optimized_cv", "").split("===")
    for section in sections:
        if not section.strip():
            continue
        lines = section.strip().split("\n")
        section_title = lines[0].replace("===", "").strip()
        
        # Section Heading
        story.append(Paragraph(section_title, heading_style))
        story.append(HRFlowable(width="30%", thickness=1, color=accent_color, hAlign='LEFT', spaceBefore=1, spaceAfter=8))
        
        # Section Text Structural Building Core
        body_text = "\n".join(lines[1:])
        for paragraph_line in body_text.split("\n"):
            if paragraph_line.strip():
                # Format bullets cleanly if they start with a hyphen or bullet point character
                if paragraph_line.strip().startswith("-") or paragraph_line.strip().startswith("•"):
                    clean_line = "• " + paragraph_line.strip().lstrip("- •")
                    story.append(Paragraph(clean_line, ParagraphStyle('CVBullet', parent=body_style, leftIndent=12, firstLineIndent=-8)))
                else:
                    story.append(Paragraph(paragraph_line.strip(), body_style))
                    
    doc.build(story)
    pdf_buffer.seek(0)
    return pdf_buffer.getvalue()

def generate_styled_docx(style_type, name, content_dict):
    """
    Sovereign Word Engine: Builds structurally layout-mapped DOCX templates natively.
    """
    doc = Document()
    
    # Setup global layout rules spacing variables
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(0.5)
        section.bottom_margin = Inches(0.5)
        section.left_margin = Inches(0.5)
        section.right_margin = Inches(0.5)

    # Inject Header Block
    title = doc.add_paragraph()
    run = title.add_run(name.upper())
    run.font.name = 'Arial'
    run.font.size = Pt(24)
    run.font.bold = True
    
    # Configure accents based on chosen structural profile style tier template match
    color_map = {
        "professional": RGBColor(30, 58, 138),
        "modern": RGBColor(6, 95, 70),
        "traditional": RGBColor(0, 0, 0)
    }
    target_color = color_map.get(style_type, RGBColor(0,0,0))
    run.font.color.rgb = target_color

    cv_sections = content_dict.get("optimized_cv", "").split("===")
    for section in cv_sections:
        if not section.strip():
            continue
        lines = section.strip().split("\n")
        section_title = lines[0].replace("===", "").strip()
        
        # Section Heading Layout Additions
        h = doc.add_paragraph()
        hrun = h.add_run(section_title)
        hrun.font.name = 'Arial'
        hrun.font.size = Pt(14)
        hrun.font.bold = True
        hrun.font.color.rgb = target_color
        h.paragraph_format.space_before = Pt(12)
        h.paragraph_format.space_after = Pt(4)
        
        body_text = "\n".join(lines[1:])
        for line in body_text.split("\n"):
            if line.strip():
                p = doc.add_paragraph()
                p.paragraph_format.space_after = Pt(4)
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

# --- Upgraded Live Route Receiver Mapping File Streams ---
@app.route('/api/download/<fmt>')
def download_compiled_file(fmt):
    user = get_session_user()
    style_selection = request.args.get("style", "professional") # Defaults safely to Corporate Professional
    
    # Fallback mock container configuration array parameters if analysis step hasn't generated fields yet
    if not user.get("optimized_cv"):
        user["optimized_cv"] = "=== PROFESSIONAL EXPERIENCE ===\n- Managed high-end server configurations across infrastructure lines.\n- Handled enterprise operational targets smoothly.\n=== CORE EXPERTISE MATRIX ===\n- Project Scaling\n- Financial Risk Allocation Control"

    if fmt == "pdf":
        pdf_bytes = generate_pdf_bytes_styled(style_selection, user.get("name", "Applicant Core"), user)
        return send_file(io.BytesIO(pdf_bytes), mimetype='application/pdf', as_attachment=True, download_name=f'Stormcore_{style_selection}_Layout.pdf')
        
    elif fmt == "docx":
        # Imports localized dependencies inline safely within execution context limits
        from docx.shared import Inches, Pt, RGBColor
        docx_bytes = generate_docx_bytes_styled(style_selection, user.get("name", "Applicant Core"), user)
        return send_file(io.BytesIO(docx_bytes), mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document', as_attachment=True, download_name=f'Stormcore_{style_selection}_Layout.docx')
        
    # Standard text file and csv fallback structures remain completely intact below...
    return redirect('/dashboard/customer')
