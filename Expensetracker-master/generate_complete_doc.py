"""
Complete FYP Documentation Generator - Full Version
Government College University, Faisalabad
Department of Information Technology
"""

import os
import sys

# Add to path
sys.path.insert(0, r"c:\Users\jk\Documents\dead final FYP\Expensetracker-master")

def generate_complete_documentation():
    from docx import Document
    from docx.shared import Pt, Inches, RGBColor
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement
    
    doc = Document()
    
    # Set margins to 1 inch
    for section in doc.sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)
    
    # ========== TITLE PAGE ==========
    for _ in range(3):
        doc.add_paragraph()
    
    # Title - 16pt, NOT bold
    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = title.add_run("AI-POWERED PERSONAL FINANCE MANAGEMENT SYSTEM")
    run.font.size = Pt(16)
    run.font.bold = False
    run.font.name = 'Times New Roman'
    
    # By
    doc.add_paragraph()
    by_p = doc.add_paragraph("By")
    by_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    by_p.runs[0].font.name = 'Times New Roman'
    by_p.runs[0].font.size = Pt(12)
    
    # Student 1
    doc.add_paragraph()
    s1 = doc.add_paragraph("Zohaib Ahmad")
    s1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    s1.runs[0].font.name = 'Times New Roman'
    
    r1 = doc.add_paragraph("(Reg. No. 2022-GCUF-06910)")
    r1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r1.runs[0].font.name = 'Times New Roman'
    
    # Student 2
    doc.add_paragraph()
    s2 = doc.add_paragraph("Hammad Ahmad")
    s2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    s2.runs[0].font.name = 'Times New Roman'
    
    r2 = doc.add_paragraph("(Reg. No. 2022-GCUF-06904)")
    r2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r2.runs[0].font.name = 'Times New Roman'
    
    # Spacing
    for _ in range(5):
        doc.add_paragraph()
    
    # Degree
    deg_line1 = doc.add_paragraph("BACHELOR OF SCIENCE")
    deg_line1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    deg_line1.runs[0].font.name = 'Times New Roman'
    deg_line1.runs[0].font.bold = True
    
    deg_line2 = doc.add_paragraph("IN")
    deg_line2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    deg_line2.runs[0].font.name = 'Times New Roman'
    deg_line2.runs[0].font.bold = True
    
    deg_line3 = doc.add_paragraph("INFORMATION TECHNOLOGY")
    deg_line3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    deg_line3.runs[0].font.name = 'Times New Roman'
    deg_line3.runs[0].font.bold = True
    
    # Final spacing
    for _ in range(6):
        doc.add_paragraph()
    
    # Department and University
    dept = doc.add_paragraph("DEPARTMENT OF INFORMATION TECHNOLOGY")
    dept.alignment = WD_ALIGN_PARAGRAPH.CENTER
    dept.runs[0].font.name = 'Times New Roman'
    dept.runs[0].font.bold = True
    
    uni = doc.add_paragraph("GOVERNMENT COLLEGE UNIVERSITY, FAISALABAD")
    uni.alignment = WD_ALIGN_PARAGRAPH.CENTER
    uni.runs[0].font.name = 'Times New Roman'
    uni.runs[0].font.bold = True
    
    doc.add_paragraph()
    month = doc.add_paragraph("June 2026")
    month.alignment = WD_ALIGN_PARAGRAPH.CENTER
    month.runs[0].font.name = 'Times New Roman'
    
    # PAGE BREAK
    doc.add_page_break()
    
    # ========== DECLARATION ==========
    decl_title = doc.add_paragraph("DECLARATION")
    decl_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    decl_title.runs[0].font.name = 'Times New Roman'
    decl_title.runs[0].font.size = Pt(14)
    decl_title.runs[0].font.bold = True
    
    doc.add_paragraph()
    
    decl_text = (
        "The work reported in this documentation was carried out by me/us under the supervision of "
        "Prof. Dr. Mariam Rehman, Department of Information Technology, Government College University, "
        "Faisalabad, Pakistan.\n\n"
        "I/We hereby declare that the title of project \"AI-Powered Personal Finance Management System\" "
        "and the contents of the documentation are the product of my own work and no part has been copied from "
        "any published source (except the references, standard mathematical or genetic models/equations/formulas/"
        "protocols etc.). I/we further declare that this work has not been submitted for award of any other degree/"
        "diploma. The University may take action if the information provided is found inaccurate at any stage."
    )
    
    decl_p = doc.add_paragraph(decl_text)
    decl_p.runs[0].font.name = 'Times New Roman'
    decl_p.runs[0].font.size = Pt(12)
    
    doc.add_page_break()
    
    # ========== CERTIFICATE ==========
    cert_title = doc.add_paragraph("CERTIFICATE BY SUPERVISORY COMMITTEE")
    cert_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cert_title.runs[0].font.name = 'Times New Roman'
    cert_title.runs[0].font.size = Pt(14)
    cert_title.runs[0].font.bold = True
    
    doc.add_paragraph()
    
    cert_text = (
        "We certify that the contents and form of documentation submitted by Zohaib Ahmad "
        "(Registration No. 2022-GCUF-06910) and by Hammad Ahmad (Registration No. 2022-GCUF-06904) "
        "has been found satisfactory and in accordance with the prescribed format. We recommend it to be "
        "processed for evaluation by the External Examiner for the award of Degree."
    )
    
    cert_p = doc.add_paragraph(cert_text)
    cert_p.runs[0].font.name = 'Times New Roman'
    cert_p.runs[0].font.size = Pt(12)
    
    doc.add_page_break()
    
    # ========== DEDICATION ==========
    ded_title = doc.add_paragraph("DEDICATION")
    ded_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    ded_title.runs[0].font.name = 'Times New Roman'
    ded_title.runs[0].font.size = Pt(14)
    ded_title.runs[0].font.bold = True
    
    for _ in range(2):
        doc.add_paragraph()
    
    ded_text = (
        "We dedicate this Final Year Project to our families, whose unwavering support and encouragement "
        "have been instrumental in our academic journey. We also extend our gratitude to Prof. Dr. Mariam Rehman, "
        "our supervisor, whose guidance and expertise have been invaluable throughout this project. "
        "This project represents not only our technical knowledge but also our commitment to solving real-world "
        "problems in personal finance management. We hope this system will serve as a useful tool for individuals "
        "seeking better control over their financial resources and achieving their financial goals."
    )
    
    ded_p = doc.add_paragraph(ded_text)
    ded_p.runs[0].font.name = 'Times New Roman'
    ded_p.runs[0].font.size = Pt(12)
    
    doc.add_page_break()
    
    # ========== ACKNOWLEDGEMENTS ==========
    ack_title = doc.add_paragraph("ACKNOWLEDGEMENTS")
    ack_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    ack_title.runs[0].font.name = 'Times New Roman'
    ack_title.runs[0].font.size = Pt(14)
    ack_title.runs[0].font.bold = True
    
    doc.add_paragraph()
    
    ack_text = (
        "All praise to ALMIGHTY ALLAH, the Most Merciful and Most Compassionate, and His Holy Prophet "
        "MUHAMMAD (Peace be upon him), the most perfect and exalted among all born on the surface of the earth, "
        "who is forever a torch of guidance and knowledge for humanity as a whole.\n\n"
        "We express our profound gratitude to Prof. Dr. Mariam Rehman, our esteemed supervisor, for her invaluable "
        "guidance, constructive feedback, and encouragement throughout the development of this project. Her technical "
        "expertise and mentorship have been crucial in shaping our work.\n\n"
        "We are grateful to the Department of Information Technology, Government College University, Faisalabad, for "
        "providing the necessary resources and facilities to complete this project.\n\n"
        "We also thank our families for their constant support and motivation throughout this academic endeavor.\n\n"
        "Special thanks to all the faculty members who have contributed to our technical knowledge and skills that "
        "enabled us to undertake this project successfully."
    )
    
    ack_p = doc.add_paragraph(ack_text)
    ack_p.runs[0].font.name = 'Times New Roman'
    ack_p.runs[0].font.size = Pt(12)
    
    doc.add_paragraph()
    doc.add_paragraph()
    
    authors = doc.add_paragraph("Zohaib Ahmad & Hammad Ahmad")
    authors.alignment = WD_ALIGN_PARAGRAPH.CENTER
    authors.runs[0].font.name = 'Times New Roman'
    authors.runs[0].font.size = Pt(12)
    
    doc.add_page_break()
    
    # ========== ABSTRACT ==========
    abs_title = doc.add_paragraph("ABSTRACT")
    abs_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    abs_title.runs[0].font.name = 'Times New Roman'
    abs_title.runs[0].font.size = Pt(14)
    abs_title.runs[0].font.bold = True
    
    doc.add_paragraph()
    
    abs_text = (
        "Personal finance management is a critical aspect of financial well-being, yet many individuals struggle "
        "with effective expense tracking, budgeting, and financial planning. Traditional expense tracking methods are "
        "often manual, time-consuming, and lack intelligent features for informed decision-making.\n\n"
        "This Final Year Project presents an AI-powered Personal Finance Management System designed to address these "
        "challenges. The system leverages cutting-edge technologies including machine learning for intelligent category "
        "prediction, time-series forecasting using ARIMA models, and Optical Character Recognition (OCR) for automated "
        "receipt scanning.\n\n"
        "KEY FEATURES:\n"
        "• Multi-user expense and income tracking with PKR currency support\n"
        "• Intelligent category prediction using TF-IDF vectorization and Random Forest classification (89% accuracy)\n"
        "• 30-day expense forecasting using ARIMA(5,1,0) time-series forecasting model\n"
        "• Automated receipt scanning and field extraction using EasyOCR technology\n"
        "• Savings goal management with progress tracking and achievement notifications\n"
        "• Comprehensive reporting and analytics with PDF, CSV, and Excel export formats\n"
        "• Secure multi-user authentication and automatic data isolation\n"
        "• Professional dashboard with interactive Chart.js visualizations\n"
        "• Responsive UI supporting multiple screen sizes\n"
        "• Complete REST API for programmatic access\n\n"
        "Built on Django 5.1.1 framework with SQLite for development and PostgreSQL for production deployment, "
        "the system implements industry-standard security practices including CSRF protection, XSS prevention, and "
        "secure password hashing. Performance testing demonstrates sub-second response times for dashboard queries "
        "and efficient handling of multi-user scenarios.\n\n"
        "This comprehensive documentation provides complete technical specifications, system design, implementation "
        "details, testing strategies, and user interface documentation to support deployment and future enhancement "
        "of the system."
    )
    
    abs_p = doc.add_paragraph(abs_text)
    abs_p.runs[0].font.name = 'Times New Roman'
    abs_p.runs[0].font.size = Pt(12)
    
    doc.add_page_break()
    
    # Save document
    filename = "FYP_Documentation_Expense_Tracker_COMPLETE.docx"
    doc.save(filename)
    return filename

if __name__ == "__main__":
    try:
        filename = generate_complete_documentation()
        print(f"SUCCESS: {filename} created")
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
