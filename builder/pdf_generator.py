from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
from io import BytesIO

def generate_pdf(data):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=LETTER)
    width, height = LETTER
    y = height - 50

    # Header
    c.setFont("Helvetica-Bold", 20)
    c.drawString(50, y, data['name'])
    y -= 25

    c.setFont("Helvetica", 10)
    c.drawString(50, y, f"Email: {data['email']} | Phone: {data['phone']}")
    y -= 15
    c.drawString(50, y, f"LinkedIn: {data['linkedin']} | GitHub: {data['github']}")
    y -= 25
    c.line(50, y, width - 50, y)
    y -= 20

    # Education
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Education")
    y -= 15
    c.setFont("Helvetica", 10)
    c.drawString(60, y, f"{data['degree']}, {data['university']} ({data['grad_year']})")
    y -= 30
    c.line(50, y, width - 50, y)
    y -= 20

    # Experience
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Experience")
    y -= 15
    c.setFont("Helvetica", 10)
    text = c.beginText(60, y)
    for line in data['experience'].split('\n'):
        text.textLine(f"• {line.strip()}")
    c.drawText(text)
    y = text.getY() - 10
    c.line(50, y, width - 50, y)
    y -= 20

    # Projects
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Projects")
    y -= 15
    c.setFont("Helvetica", 10)
    c.drawString(60, y, data['project_title'])
    y -= 15
    text = c.beginText(60, y)
    for line in data['project_desc'].split('\n'):
        text.textLine(f"• {line.strip()}")
    c.drawText(text)
    y = text.getY() - 10
    c.line(50, y, width - 50, y)
    y -= 20

    # Skills
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Skills")
    y -= 15
    c.setFont("Helvetica", 10)
    c.drawString(60, y, data['skills'])

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer
