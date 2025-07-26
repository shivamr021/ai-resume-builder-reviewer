import streamlit as st
from io import BytesIO
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
from builder.form_fields import (
    basic_fields,
    education_section,
    experience_section,
    project_section,
    skills_section,
    additional_sections,
    show_form_tips
)

def handle_resume_form():
    # Show helpful tips
    show_form_tips()

    # Add Education button (outside the form, above the form)
    add_col, _ = st.columns([1, 5])
    with add_col:
        if st.button("➕ Add Education", key="add_education", help="Add another education entry"):
            if "education_entries" not in st.session_state:
                st.session_state.education_entries = []
            st.session_state.education_entries.append({
                "degree": "",
                "institution": "",
                "start": "",
                "end": "",
                "grade": ""
            })
            st.rerun()

    with st.form("resume_form"):
        # Form Sections
        name, email, phone, linkedin, github = basic_fields()
        education_section()  # Only renders fields
        experience = experience_section()
        project_title, project_desc = project_section()
        skills = skills_section()
        volunteering, hobbies, certifications = additional_sections()

        submitted = st.form_submit_button("📄 Generate Resume")

    # Remove buttons for each education entry (outside the form, after the form)
    if "education_entries" in st.session_state:
        for idx in range(len(st.session_state.education_entries)):
            if len(st.session_state.education_entries) > 1:
                remove_col, _ = st.columns([1, 5])
                with remove_col:
                    if st.button(f"🗑️ Remove Entry {idx+1}", key=f"remove_edu_{idx}", help="Remove this education entry"):
                        st.session_state.education_entries.pop(idx)
                        st.rerun()

    if submitted:
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=LETTER)
        width, height = LETTER
        y = height - 50

        # Header
        c.setFont("Helvetica-Bold", 20)
        c.drawString(50, y, name)
        y -= 25

        c.setFont("Helvetica", 10)
        c.drawString(50, y, f"Email: {email} | Phone: {phone}")
        y -= 15
        c.drawString(50, y, f"LinkedIn: {linkedin} | GitHub: {github}")
        y -= 25
        c.line(50, y, width - 50, y)
        y -= 20

        # Education
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, "Education")
        y -= 15
        c.setFont("Helvetica", 10)

        for edu in st.session_state.education_entries:
            edu_str = f"{edu.get('degree', '')}, {edu.get('institution', '')} ({edu.get('start', '')} - {edu.get('end', '')}) | Grade: {edu.get('grade', '')}"
            c.drawString(60, y, edu_str)
            y -= 15
        y -= 10
        c.line(50, y, width - 50, y)
        y -= 20

        # Experience
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, "Experience")
        y -= 15
        c.setFont("Helvetica", 10)
        text = c.beginText(60, y)
        for line in experience.split('\n'):
            if line.strip():
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
        c.drawString(60, y, f"{project_title}")
        y -= 15
        text = c.beginText(60, y)
        for line in project_desc.split('\n'):
            if line.strip():
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
        for skill in skills.split(','):
            c.drawString(60, y, f"• {skill.strip()}")
            y -= 12
        y -= 10
        c.line(50, y, width - 50, y)
        y -= 20

        # Optional: Volunteering
        if volunteering.strip():
            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, y, "Volunteering / Extra-curricular")
            y -= 15
            c.setFont("Helvetica", 10)
            text = c.beginText(60, y)
            for line in volunteering.split('\n'):
                if line.strip():
                    text.textLine(f"• {line.strip()}")
            c.drawText(text)
            y = text.getY() - 10
            c.line(50, y, width - 50, y)
            y -= 20

        # Optional: Certifications
        if certifications.strip():
            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, y, "Certifications / Courses")
            y -= 15
            c.setFont("Helvetica", 10)
            text = c.beginText(60, y)
            for line in certifications.split('\n'):
                if line.strip():
                    text.textLine(f"• {line.strip()}")
            c.drawText(text)
            y = text.getY() - 10
            c.line(50, y, width - 50, y)
            y -= 20

        # Optional: Hobbies
        if hobbies.strip():
            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, y, "Hobbies")
            y -= 15
            c.setFont("Helvetica", 10)
            for hobby in hobbies.split(','):
                c.drawString(60, y, f"• {hobby.strip()}")
                y -= 12

        # Save
        c.showPage()
        c.save()
        buffer.seek(0)

        st.download_button(
            label="📄 Download Resume as PDF",
            data=buffer,
            file_name=f"{name.strip().replace(' ', '_').lower()}_resume.pdf",
            mime="application/pdf"
        )
