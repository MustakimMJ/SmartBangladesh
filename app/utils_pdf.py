import os
from io import BytesIO
from datetime import datetime
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.pdfgen import canvas

def generate_certificate_pdf(application, user, cert_id):
    """
    Generates a beautifully designed landscape A4 PDF certificate.
    Returns a BytesIO buffer containing the PDF data.
    """
    buffer = BytesIO()
    
    # Set page to A4 landscape: width = 841.89, height = 595.27 points
    width, height = landscape(A4)
    
    p = canvas.Canvas(buffer, pagesize=landscape(A4))
    
    # ------------------ DRAW BACKGROUND & WATERMARK ------------------
    # Soft light green background fill
    p.setFillColor(colors.HexColor('#F4F9F6'))
    p.rect(0, 0, width, height, fill=True, stroke=False)
    
    # Draw faint rotated watermark text
    p.saveState()
    p.setFont("Helvetica-Bold", 40)
    p.setFillColor(colors.HexColor('#E2ECE7'))
    p.translate(width / 2, height / 2)
    p.rotate(35)
    p.drawCentredString(0, 80, "GOVERNMENT OF BANGLADESH")
    p.drawCentredString(0, 0, "SMART BANGLADESH DIGITAL SERVICES")
    p.drawCentredString(0, -80, "OFFICIAL VERIFIED DOCUMENT")
    p.restoreState()
    
    # ------------------ DRAW ORNATE BORDERS ------------------
    # Outer thick green border
    p.setStrokeColor(colors.HexColor('#006C5C'))
    p.setLineWidth(5)
    p.rect(20, 20, width - 40, height - 40, fill=False, stroke=True)
    
    # Inner thin gold border
    p.setStrokeColor(colors.HexColor('#D4AF37'))
    p.setLineWidth(2)
    p.rect(28, 28, width - 56, height - 56, fill=False, stroke=True)
    
    # Draw decorative corner squares
    p.setFillColor(colors.HexColor('#D4AF37'))
    # Top-left corner decoration
    p.rect(20, height - 35, 15, 15, fill=True, stroke=False)
    p.rect(35, height - 20, 15, 15, fill=True, stroke=False)
    # Top-right corner decoration
    p.rect(width - 35, height - 35, 15, 15, fill=True, stroke=False)
    p.rect(width - 50, height - 20, 15, 15, fill=True, stroke=False)
    # Bottom-left corner decoration
    p.rect(20, 20, 15, 15, fill=True, stroke=False)
    p.rect(35, 20, 15, 15, fill=True, stroke=False)
    # Bottom-right corner decoration
    p.rect(width - 35, 20, 15, 15, fill=True, stroke=False)
    p.rect(width - 50, 20, 15, 15, fill=True, stroke=False)
    
    # ------------------ HEADER SECTION ------------------
    # Government Title
    p.setFillColor(colors.HexColor('#006C5C'))
    p.setFont("Helvetica-Bold", 18)
    p.drawCentredString(width / 2, 530, "GOVERNMENT OF THE PEOPLE'S REPUBLIC OF BANGLADESH")
    
    # Ministry Subtitle
    p.setFillColor(colors.HexColor('#EF3B39'))
    p.setFont("Helvetica-Bold", 11)
    p.drawCentredString(width / 2, 510, "MINISTRY OF POSTS, TELECOMMUNICATIONS AND INFORMATION TECHNOLOGY")
    
    p.setFillColor(colors.HexColor('#333333'))
    p.setFont("Helvetica", 10)
    p.drawCentredString(width / 2, 495, "Smart Bangladesh Digital Services Bureau")
    
    # Decorative line under header
    p.setStrokeColor(colors.HexColor('#D4AF37'))
    p.setLineWidth(1.5)
    p.line(150, 480, width - 150, 480)
    
    # ------------------ CERTIFICATE TITLE ------------------
    # Map service type to title
    service_type = application.get('service_type', '')
    if service_type == 'birth_certificate':
        cert_title = "DIGITAL BIRTH REGISTRATION CERTIFICATE"
    elif service_type == 'death_certificate':
        cert_title = "DIGITAL DEATH REGISTRATION CERTIFICATE"
    elif service_type == 'family_certificate':
        cert_title = "DIGITAL FAMILY CERTIFICATE"
    elif service_type == 'police_clearance':
        cert_title = "DIGITAL POLICE CLEARANCE CERTIFICATE"
    else:
        cert_title = "OFFICIAL GOVERNMENT CERTIFICATE"
        
    p.setFillColor(colors.HexColor('#006C5C'))
    p.setFont("Helvetica-Bold", 22)
    p.drawCentredString(width / 2, 445, cert_title)
    
    # Unique Certificate Serial Number
    p.setFillColor(colors.HexColor('#333333'))
    p.setFont("Helvetica-Bold", 13)
    p.drawCentredString(width / 2, 420, f"Certificate Serial: {cert_id}")
    
    # ------------------ CERTIFICATION CLAUSE ------------------
    p.setFillColor(colors.HexColor('#555555'))
    p.setFont("Helvetica-Oblique", 11)
    p.drawCentredString(width / 2, 385, "This is to officially certify that the records maintained by the Digital Services Portal confirm")
    p.drawCentredString(width / 2, 368, "the registration and verification details for the citizen listed below:")
    
    # ------------------ DETAILS TABLE BACKGROUND BOX ------------------
    box_x = 100
    box_y = 150
    box_w = width - 200
    box_h = 190
    
    p.setFillColor(colors.HexColor('#FFFFFF'))
    p.setStrokeColor(colors.HexColor('#E2ECE7'))
    p.setLineWidth(1)
    p.rect(box_x, box_y, box_w, box_h, fill=True, stroke=True)
    
    # Draw double vertical partition line inside box
    p.setStrokeColor(colors.HexColor('#F2F2F2'))
    p.line(width / 2, box_y + 10, width / 2, box_y + box_h - 10)
    
    # ------------------ DYNAMIC DETAILS PRINTING ------------------
    p.setFillColor(colors.HexColor('#333333'))
    p.setFont("Helvetica-Bold", 11)
    
    # Left Column Keys
    p.drawString(130, 310, "Full Name:")
    p.drawString(130, 275, "NID / Reg Number:")
    p.drawString(130, 240, "Phone Number:")
    p.drawString(130, 205, "Address:")
    
    # Right Column Keys
    p.drawString(450, 310, "Certificate Type:")
    p.drawString(450, 275, "Date of Issue:")
    p.drawString(450, 240, "Verification Status:")
    p.drawString(450, 205, "Registration details:")
    
    # Values Styling
    p.setFont("Helvetica", 11)
    p.setFillColor(colors.HexColor('#444444'))
    
    # Left Column Values
    p.drawString(250, 310, str(user.get('name', 'N/A')))
    p.drawString(250, 275, str(user.get('nid', 'N/A')))
    p.drawString(250, 240, str(user.get('phone', 'N/A')))
    
    # For address, print neatly or wrap if too long
    addr = str(user.get('address', 'N/A'))
    if len(addr) > 30:
        p.drawString(250, 205, addr[:30] + "...")
    else:
        p.drawString(250, 205, addr)
        
    # Right Column Values
    p.drawString(580, 310, str(service_type.replace('_', ' ').title()))
    
    # Issue date formatting
    issue_date = application.get('updated_at') or application.get('created_at') or datetime.now()
    if isinstance(issue_date, str):
        p.drawString(580, 275, issue_date)
    else:
        p.drawString(580, 275, issue_date.strftime('%d %B %Y'))
        
    # Status (Verified & Active badge representation)
    p.saveState()
    p.setFillColor(colors.HexColor('#155724'))  # Dark Green
    p.setFont("Helvetica-Bold", 11)
    p.drawString(580, 240, "VERIFIED & ACTIVE")
    p.restoreState()
    
    # Details short preview
    desc = str(application.get('description', 'Official Registration'))
    if len(desc) > 32:
        p.drawString(580, 205, desc[:32] + "...")
    else:
        p.drawString(580, 205, desc)
        
    # ------------------ SEAL & SIGNATURE AREAS ------------------
    # Left Seal Area
    # Draw double circle for seal
    seal_x = 200
    seal_y = 90
    p.setStrokeColor(colors.HexColor('#006C5C'))
    p.setLineWidth(1)
    p.circle(seal_x, seal_y, 25, fill=False, stroke=True)
    p.circle(seal_x, seal_y, 22, fill=False, stroke=True)
    
    p.setFillColor(colors.HexColor('#006C5C'))
    p.setFont("Helvetica-Bold", 6)
    p.drawCentredString(seal_x, seal_y + 8, "OFFICIAL SEAL")
    p.drawCentredString(seal_x, seal_y, "GOVERNMENT")
    p.drawCentredString(seal_x, seal_y - 8, "BANGLADESH")
    
    # Right Signature Area
    sig_line_x = 530
    sig_y = 80
    p.setStrokeColor(colors.HexColor('#444444'))
    p.setLineWidth(1)
    p.line(sig_line_x, sig_y + 15, sig_line_x + 180, sig_y + 15)
    
    # Fake signature text
    p.setFillColor(colors.HexColor('#006C5C'))
    p.setFont("Courier-BoldOblique", 11)
    p.drawString(sig_line_x + 30, sig_y + 20, "DG - Digital Bureau")
    
    p.setFillColor(colors.HexColor('#444444'))
    p.setFont("Helvetica-Bold", 9)
    p.drawString(sig_line_x, sig_y, "Director General, Digital Services")
    p.setFont("Helvetica", 8)
    p.drawString(sig_line_x, sig_y - 10, "Government of the People's Republic of Bangladesh")
    
    # ------------------ FOOTER VERIFICATION SECTION ------------------
    # Verification URL instruction
    p.setFillColor(colors.HexColor('#666666'))
    p.setFont("Helvetica", 8)
    verify_url = f"http://localhost:5000/verify/{cert_id}"
    p.drawCentredString(width / 2, 45, f"This document is electronically generated and can be verified publicly.")
    p.drawCentredString(width / 2, 33, f"To verify, visit: {verify_url}")
    
    # Save the page
    p.showPage()
    p.save()
    
    buffer.seek(0)
    return buffer
