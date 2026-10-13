"""
FYP Documentation Generator for Government College University, Faisalabad
Department of Information Technology
Generates complete documentation as per university standards
"""

from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import os
from datetime import datetime

def set_line_spacing(paragraph, spacing=1.5):
    """Set line spacing for a paragraph"""
    p = paragraph._element
    pPr = p.get_or_add_pPr()
    spacing_elem = OxmlElement('w:spacing')
    spacing_elem.set(qn('w:line'), str(int(spacing * 240)))
    pPr.append(spacing_elem)

def add_page_break(doc):
    """Add page break"""
    doc.add_page_break()

def set_margins(doc, top=1, bottom=1, left=1, right=1):
    """Set document margins"""
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(top)
        section.bottom_margin = Inches(bottom)
        section.left_margin = Inches(left)
        section.right_margin = Inches(right)

def create_title_page(doc):
    """Create Title Page"""
    # Add empty lines
    for _ in range(3):
        doc.add_paragraph()
    
    # Project Title - Font Size 16, NOT bold
    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = title.add_run("AI-POWERED PERSONAL FINANCE MANAGEMENT SYSTEM")
    run.font.size = Pt(16)
    run.font.bold = False
    run.font.name = 'Times New Roman'
    
    # By
    doc.add_paragraph()
    by_para = doc.add_paragraph("By")
    by_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    by_para.runs[0].font.name = 'Times New Roman'
    by_para.runs[0].font.size = Pt(12)
    
    # Student Names and Registration Numbers
    doc.add_paragraph()
    student1 = doc.add_paragraph("Zohaib Ahmad")
    student1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    student1.runs[0].font.name = 'Times New Roman'
    student1.runs[0].font.size = Pt(12)
    
    reg1 = doc.add_paragraph("(Reg. No. 2022-GCUF-06910)")
    reg1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    reg1.runs[0].font.name = 'Times New Roman'
    reg1.runs[0].font.size = Pt(12)
    
    doc.add_paragraph()
    student2 = doc.add_paragraph("Hammad Ahmad")
    student2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    student2.runs[0].font.name = 'Times New Roman'
    student2.runs[0].font.size = Pt(12)
    
    reg2 = doc.add_paragraph("(Reg. No. 2022-GCUF-06904)")
    reg2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    reg2.runs[0].font.name = 'Times New Roman'
    reg2.runs[0].font.size = Pt(12)
    
    # Add spacing
    for _ in range(5):
        doc.add_paragraph()
    
    # Degree
    degree1 = doc.add_paragraph("BACHELOR OF SCIENCE")
    degree1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    degree1.runs[0].font.name = 'Times New Roman'
    degree1.runs[0].font.size = Pt(12)
    degree1.runs[0].font.bold = True
    
    degree2 = doc.add_paragraph("IN")
    degree2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    degree2.runs[0].font.name = 'Times New Roman'
    degree2.runs[0].font.size = Pt(12)
    degree2.runs[0].font.bold = True
    
    degree3 = doc.add_paragraph("INFORMATION TECHNOLOGY")
    degree3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    degree3.runs[0].font.name = 'Times New Roman'
    degree3.runs[0].font.size = Pt(12)
    degree3.runs[0].font.bold = True
    
    # Add spacing
    for _ in range(6):
        doc.add_paragraph()
    
    # Department and University
    dept = doc.add_paragraph("DEPARTMENT OF INFORMATION TECHNOLOGY")
    dept.alignment = WD_ALIGN_PARAGRAPH.CENTER
    dept.runs[0].font.name = 'Times New Roman'
    dept.runs[0].font.size = Pt(12)
    dept.runs[0].font.bold = True
    
    uni = doc.add_paragraph("GOVERNMENT COLLEGE UNIVERSITY, FAISALABAD")
    uni.alignment = WD_ALIGN_PARAGRAPH.CENTER
    uni.runs[0].font.name = 'Times New Roman'
    uni.runs[0].font.size = Pt(12)
    uni.runs[0].font.bold = True
    
    doc.add_paragraph()
    month = doc.add_paragraph("June 2026")
    month.alignment = WD_ALIGN_PARAGRAPH.CENTER
    month.runs[0].font.name = 'Times New Roman'
    month.runs[0].font.size = Pt(12)
    
    add_page_break(doc)

def create_declaration(doc):
    """Create Declaration Page"""
    title = doc.add_paragraph("DECLARATION")
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title.runs[0].font.name = 'Times New Roman'
    title.runs[0].font.size = Pt(14)
    title.runs[0].font.bold = True
    
    doc.add_paragraph()
    
    declaration_text = (
        "The work reported in this documentation was carried out by me/us under the supervision of "
        "Prof. Dr. Mariam Rehman, Department of Information Technology, Government College University, "
        "Faisalabad, Pakistan.\n\n"
        "I/We hereby declare that the title of project \"AI-Powered Personal Finance Management System\" "
        "and the contents of the documentation are the product of my own work and no part has been copied from "
        "any published source (except the references, standard mathematical or genetic models/equations/formulas/"
        "protocols etc.). I/we further declare that this work has not been submitted for award of any other degree/"
        "diploma. The University may take action if the information provided is found inaccurate at any stage."
    )
    
    decl = doc.add_paragraph(declaration_text)
    set_line_spacing(decl, 1.5)
    decl.runs[0].font.name = 'Times New Roman'
    decl.runs[0].font.size = Pt(12)
    
    doc.add_paragraph()
    doc.add_paragraph()
    
    # Signature lines
    sig_table = doc.add_table(rows=4, cols=2)
    sig_table.autofit = False
    
    # Student 1
    sig_table.rows[0].cells[0].text = "Signature of Student"
    sig_table.rows[1].cells[0].text = "Zohaib Ahmad (2022-GCUF-06910)"
    
    # Student 2
    sig_table.rows[0].cells[1].text = "Signature of Student"
    sig_table.rows[1].cells[1].text = "Hammad Ahmad (2022-GCUF-06904)"
    
    # Format signature table
    for row in sig_table.rows:
        for cell in row.cells:
            for paragraph in cell.paragraphs:
                paragraph.runs[0].font.name = 'Times New Roman'
                paragraph.runs[0].font.size = Pt(11)
    
    add_page_break(doc)

def create_certificate(doc):
    """Create Certificate by Supervisory Committee"""
    title = doc.add_paragraph("CERTIFICATE BY SUPERVISORY COMMITTEE")
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title.runs[0].font.name = 'Times New Roman'
    title.runs[0].font.size = Pt(14)
    title.runs[0].font.bold = True
    
    doc.add_paragraph()
    
    cert_text = (
        "We certify that the contents and form of documentation submitted by Zohaib Ahmad "
        "(Registration No. 2022-GCUF-06910) and by Hammad Ahmad (Registration No. 2022-GCUF-06904) "
        "has been found satisfactory and in accordance with the prescribed format. We recommend it to be "
        "processed for evaluation by the External Examiner for the award of Degree."
    )
    
    cert = doc.add_paragraph(cert_text)
    set_line_spacing(cert, 1.5)
    cert.runs[0].font.name = 'Times New Roman'
    cert.runs[0].font.size = Pt(12)
    
    doc.add_paragraph()
    doc.add_paragraph()
    doc.add_paragraph()
    
    # Certificate table
    cert_table = doc.add_table(rows=8, cols=1)
    cert_table.autofit = False
    
    rows = cert_table.rows
    rows[0].cells[0].text = "Signature of Supervisor: ____________________"
    rows[1].cells[0].text = "Name: ____________________________________"
    rows[2].cells[0].text = "Designation with Stamp: ___________________"
    
    rows[3].cells[0].text = "Member of Supervisory Committee"
    rows[4].cells[0].text = "Signature: _________________________________"
    rows[5].cells[0].text = "Name: ____________________________________"
    rows[6].cells[0].text = "Designation with Stamp: ___________________"
    
    rows[7].cells[0].text = "Chairperson"
    
    for row in cert_table.rows:
        for cell in row.cells:
            for paragraph in cell.paragraphs:
                paragraph.runs[0].font.name = 'Times New Roman'
                paragraph.runs[0].font.size = Pt(11)
    
    add_page_break(doc)

def create_dedication(doc):
    """Create Dedication Page"""
    title = doc.add_paragraph("DEDICATION")
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title.runs[0].font.name = 'Times New Roman'
    title.runs[0].font.size = Pt(14)
    title.runs[0].font.bold = True
    
    for _ in range(2):
        doc.add_paragraph()
    
    dedication_text = (
        "We dedicate this Final Year Project to our families, whose unwavering support and encouragement "
        "have been instrumental in our academic journey. We also extend our gratitude to Prof. Dr. Mariam Rehman, "
        "our supervisor, whose guidance and expertise have been invaluable throughout this project. "
        "This project represents not only our technical knowledge but also our commitment to solving real-world "
        "problems in personal finance management. We hope this system will serve as a useful tool for individuals "
        "seeking better control over their financial resources."
    )
    
    dedic = doc.add_paragraph(dedication_text)
    set_line_spacing(dedic, 1.5)
    dedic.runs[0].font.name = 'Times New Roman'
    dedic.runs[0].font.size = Pt(12)
    
    add_page_break(doc)

def create_acknowledgements(doc):
    """Create Acknowledgements Page"""
    title = doc.add_paragraph("ACKNOWLEDGEMENTS")
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title.runs[0].font.name = 'Times New Roman'
    title.runs[0].font.size = Pt(14)
    title.runs[0].font.bold = True
    
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
    
    ack = doc.add_paragraph(ack_text)
    set_line_spacing(ack, 1.5)
    ack.runs[0].font.name = 'Times New Roman'
    ack.runs[0].font.size = Pt(12)
    
    doc.add_paragraph()
    doc.add_paragraph()
    
    authors = doc.add_paragraph("Zohaib Ahmad & Hammad Ahmad")
    authors.alignment = WD_ALIGN_PARAGRAPH.CENTER
    authors.runs[0].font.name = 'Times New Roman'
    authors.runs[0].font.size = Pt(12)
    
    add_page_break(doc)

def create_abstract(doc):
    """Create Abstract"""
    title = doc.add_paragraph("ABSTRACT")
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title.runs[0].font.name = 'Times New Roman'
    title.runs[0].font.size = Pt(14)
    title.runs[0].font.bold = True
    
    doc.add_paragraph()
    
    abstract_text = (
        "Personal finance management is a critical aspect of financial well-being, yet many individuals struggle "
        "with effective expense tracking, budgeting, and financial planning. Traditional expense tracking methods are "
        "often manual, time-consuming, and lack intelligent features for informed decision-making.\n\n"
        "This Final Year Project presents an AI-powered Personal Finance Management System designed to address these "
        "challenges. The system leverages cutting-edge technologies including machine learning for intelligent category "
        "prediction, time-series forecasting using ARIMA models, and Optical Character Recognition (OCR) for automated "
        "receipt scanning.\n\n"
        "The system provides comprehensive features including:\n"
        "• Multi-user expense and income tracking with PKR currency support\n"
        "• Intelligent category prediction using TF-IDF vectorization and Random Forest classification\n"
        "• 30-day expense forecasting using ARIMA(5,1,0) time-series model\n"
        "• Automated receipt scanning and field extraction using EasyOCR technology\n"
        "• Savings goal management with progress tracking\n"
        "• Comprehensive reporting and analytics with PDF/CSV/Excel export\n"
        "• Secure multi-user authentication and data isolation\n"
        "• Professional dashboard with interactive charts and visualizations\n\n"
        "Built on Django framework with SQLite database for development and PostgreSQL for production, the system "
        "implements industry-standard security practices including CSRF protection, XSS prevention, and secure authentication. "
        "The application demonstrates scalability, achieving sub-second response times for dashboard queries and handling "
        "multi-user scenarios efficiently.\n\n"
        "This documentation provides comprehensive technical specifications, system design, implementation details, testing "
        "strategies, and user interface documentation to support deployment and future enhancement of the system."
    )
    
    abs = doc.add_paragraph(abstract_text)
    set_line_spacing(abs, 1.5)
    abs.runs[0].font.name = 'Times New Roman'
    abs.runs[0].font.size = Pt(12)
    
    add_page_break(doc)

def create_toc_placeholder(doc):
    """Create Table of Contents placeholder"""
    toc_title = doc.add_paragraph("TABLE OF CONTENTS")
    toc_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    toc_title.runs[0].font.name = 'Times New Roman'
    toc_title.runs[0].font.size = Pt(14)
    toc_title.runs[0].font.bold = True
    
    doc.add_paragraph()
    
    toc_items = [
        ("FRONT MATTER", None),
        ("Declaration", "ii"),
        ("Certificate by Supervisory Committee", "iii"),
        ("Dedication", "iv"),
        ("Acknowledgements", "v"),
        ("Abstract", "vi"),
        ("", ""),
        ("CHAPTER 1: SOFTWARE REQUIREMENT SPECIFICATION", "1"),
        ("1.1 Introduction", "1"),
        ("1.2 Project Objectives", "2"),
        ("1.3 Scope of the System", "3"),
        ("1.4 Technical Feasibility", "4"),
        ("1.5 Economic Feasibility", "5"),
        ("1.6 Operational Feasibility", "6"),
        ("1.7 Stakeholders", "7"),
        ("1.8 Users of the System", "8"),
        ("1.9 Functional Requirements", "9"),
        ("1.10 Non-Functional Requirements", "12"),
        ("1.11 Schedule of the Project", "13"),
        ("", ""),
        ("CHAPTER 2: ANALYSIS", "14"),
        ("2.1 Use Case Model", "14"),
        ("2.2 System Sequence Diagrams", "18"),
        ("2.3 Domain Model", "25"),
        ("", ""),
        ("CHAPTER 3: PROJECT DESIGN", "26"),
        ("3.1 Introduction", "26"),
        ("3.2 Design Class Diagram", "27"),
        ("3.3 Entity Relationship Diagram", "28"),
        ("3.4 Sequence Diagrams", "29"),
        ("3.5 System Architecture Diagram", "35"),
        ("3.6 Data Flow Diagrams", "36"),
        ("", ""),
        ("CHAPTER 4: IMPLEMENTATION", "37"),
        ("4.1 Tools & Technologies Used", "37"),
        ("4.2 System Modules Description", "39"),
        ("4.3 Code/Algorithm of Main Scenarios", "42"),
        ("", ""),
        ("CHAPTER 5: SYSTEM TESTING", "50"),
        ("5.1 Test Cases", "50"),
        ("5.2 Testing Types", "55"),
        ("5.3 Test Summary Report", "57"),
        ("", ""),
        ("CHAPTER 6: USER INTERFACES", "58"),
    ]
    
    for item, page in toc_items:
        if item == "":
            doc.add_paragraph()
        else:
            p = doc.add_paragraph(item)
            p.paragraph_format.left_indent = Inches(0.5 if item.startswith("1.") or item.startswith("2.") or item.startswith("3.") or item.startswith("4.") or item.startswith("5.") else 0)
            p.runs[0].font.name = 'Times New Roman'
            p.runs[0].font.size = Pt(12)
            if page:
                p.runs[0].text = item + " " * (80 - len(item) - len(page)) + page
    
    add_page_break(doc)

def create_list_of_figures(doc):
    """Create List of Figures"""
    lof_title = doc.add_paragraph("LIST OF FIGURES")
    lof_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    lof_title.runs[0].font.name = 'Times New Roman'
    lof_title.runs[0].font.size = Pt(14)
    lof_title.runs[0].font.bold = True
    
    doc.add_paragraph()
    
    figures = [
        ("Figure 1", "Agile Development Model", "13"),
        ("Figure 2", "Use Case Diagram", "14"),
        ("Figure 3", "System Sequence Diagram - User Registration & Login", "18"),
        ("Figure 4", "System Sequence Diagram - Add Expense with ML Prediction", "19"),
        ("Figure 5", "System Sequence Diagram - Receipt Scanning (OCR)", "20"),
        ("Figure 6", "System Sequence Diagram - Income Entry and Summary", "21"),
        ("Figure 7", "System Sequence Diagram - Expense Forecast Generation", "22"),
        ("Figure 8", "System Sequence Diagram - Goal Creation and Tracking", "23"),
        ("Figure 9", "Domain Model", "25"),
        ("Figure 10", "Design Class Diagram", "27"),
        ("Figure 11", "Entity Relationship Diagram", "28"),
        ("Figure 12", "Design Sequence Diagram - Expense Processing", "29"),
        ("Figure 13", "System Architecture Diagram (3-tier MVC)", "35"),
        ("Figure 14", "Data Flow Diagram - Level 0 (Context)", "36"),
        ("Figure 15", "Data Flow Diagram - Level 1", "37"),
        ("Figure 16", "Login/Register Interface", "58"),
        ("Figure 17", "Dashboard Overview", "59"),
        ("Figure 18", "Add Expense Interface", "60"),
        ("Figure 19", "Category Prediction Feature", "61"),
        ("Figure 20", "Expense Forecast Display", "62"),
        ("Figure 21", "Receipt Scanning Interface", "63"),
        ("Figure 22", "Goals Management Interface", "64"),
        ("Figure 23", "Income Tracking Interface", "65"),
        ("Figure 24", "Admin Panel", "66"),
    ]
    
    for fig_num, fig_title, page in figures:
        p = doc.add_paragraph(f"{fig_num}: {fig_title}")
        p.runs[0].font.name = 'Times New Roman'
        p.runs[0].font.size = Pt(12)
        p.runs[0].text = f"{fig_num}: {fig_title}" + " " * (80 - len(f"{fig_num}: {fig_title}") - len(page)) + page
    
    add_page_break(doc)

def create_list_of_tables(doc):
    """Create List of Tables"""
    lot_title = doc.add_paragraph("LIST OF TABLES")
    lot_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    lot_title.runs[0].font.name = 'Times New Roman'
    lot_title.runs[0].font.size = Pt(14)
    lot_title.runs[0].font.bold = True
    
    doc.add_paragraph()
    
    tables = [
        ("Table 1", "Functional Requirements List", "9"),
        ("Table 2", "FR01 - Expense Tracking", "9"),
        ("Table 3", "FR02 - Income Management", "10"),
        ("Table 4", "FR03 - Expense Forecasting", "10"),
        ("Table 5", "FR04 - Receipt Scanning", "11"),
        ("Table 6", "FR05 - Goal Management", "11"),
        ("Table 7", "Non-Functional Requirements", "12"),
        ("Table 8", "UC01 - User Registration", "15"),
        ("Table 9", "UC02 - User Login", "16"),
        ("Table 10", "UC03 - Add Expense", "16"),
        ("Table 11", "UC04 - View Expense Forecast", "17"),
        ("Table 12", "UC05 - Scan Receipt", "17"),
        ("Table 13", "UC06 - Manage Goal", "18"),
        ("Table 14", "Database Schema - User Table", "30"),
        ("Table 15", "Database Schema - Expense Table", "30"),
        ("Table 16", "Database Schema - Income Table", "31"),
        ("Table 17", "Database Schema - Goal Table", "31"),
        ("Table 18", "Database Schema - Category Table", "32"),
        ("Table 19", "Database Schema - UserPreference Table", "32"),
        ("Table 20", "Technologies and Versions", "37"),
        ("Table 21", "Test Case TC01 - User Registration", "50"),
        ("Table 22", "Test Case TC02 - Add Expense", "51"),
        ("Table 23", "Test Case TC03 - Forecast Generation", "52"),
        ("Table 24", "Test Summary Report", "57"),
    ]
    
    for tab_num, tab_title, page in tables:
        p = doc.add_paragraph(f"{tab_num}: {tab_title}")
        p.runs[0].font.name = 'Times New Roman'
        p.runs[0].font.size = Pt(12)
        p.runs[0].text = f"{tab_num}: {tab_title}" + " " * (80 - len(f"{tab_num}: {tab_title}") - len(page)) + page
    
    add_page_break(doc)

# Create document with all sections
if __name__ == "__main__":
    doc = Document()
    set_margins(doc)
    
    # Set default font
    style = doc.styles['Normal']
    style.font.name = 'Times New Roman'
    style.font.size = Pt(12)
    
    print("Creating Title Page...")
    create_title_page(doc)
    
    print("Creating Declaration...")
    create_declaration(doc)
    
    print("Creating Certificate...")
    create_certificate(doc)
    
    print("Creating Dedication...")
    create_dedication(doc)
    
    print("Creating Acknowledgements...")
    create_acknowledgements(doc)
    
    print("Creating Abstract...")
    create_abstract(doc)
    
    print("Creating Table of Contents...")
    create_toc_placeholder(doc)
    
    print("Creating List of Figures...")
    create_list_of_figures(doc)
    
    print("Creating List of Tables...")
    create_list_of_tables(doc)
    
    # Save document
    output_path = "FYP_Documentation_Expense_Tracker.docx"
    doc.save(output_path)
    print(f"✅ Document saved: {output_path}")
    print(f"📄 Location: {os.path.abspath(output_path)}")
