import streamlit as st

def show_form_tips():
    """Display helpful tips for users"""
    with st.expander("💡 Tips for a Great Resume", expanded=False):
        st.markdown("""
        **📝 Writing Tips:**
        - Use action verbs (e.g., Developed, Implemented, Led, Managed)
        - Include quantifiable achievements (e.g., "Increased efficiency by 25%")
        - Keep bullet points concise and impactful
        - Use industry-specific keywords relevant to your target role
        
        **🎯 ATS Optimization:**
        - Include relevant keywords from job descriptions
        - Use standard section headings
        - Avoid graphics, tables, or complex formatting
        - Keep your resume to 1-2 pages maximum
        
        **📋 Format Guidelines:**
        - Use bullet points for experience and projects
        - Separate skills with commas
        - Include dates in YYYY format for education
        - Provide specific examples and outcomes
        """)

def basic_fields():
    st.subheader("👤 Basic Information")
    
    # Use columns for better layout
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Full Name", key="name", placeholder="John Doe")
        email = st.text_input("Email", key="email", placeholder="john.doe@email.com")
        phone = st.text_input("Phone Number", key="phone", placeholder="+1 (555) 123-4567")
    with col2:
        linkedin = st.text_input("LinkedIn URL", key="linkedin", placeholder="https://linkedin.com/in/johndoe")
        github = st.text_input("GitHub URL", key="github", placeholder="https://github.com/johndoe")
        
    return name, email, phone, linkedin, github

def education_section():
    st.subheader("🎓 Education")

    if "education_entries" not in st.session_state:
        st.session_state.education_entries = [{
            "degree": "",
            "institution": "",
            "start": "",
            "end": "",
            "grade": ""
        }]

    # Display education entries
    for idx, entry in enumerate(st.session_state.education_entries):
        with st.container():
            st.markdown("---")
            entry_col1, entry_col2 = st.columns([4, 1])
            with entry_col1:
                st.markdown(f"**Education Entry {idx + 1}**")
            with entry_col2:
                st.markdown("")  # Placeholder for remove button, handled outside form
            col1, col2 = st.columns(2)
            with col1:
                entry["degree"] = st.text_input("Degree", value=entry["degree"], key=f"degree_{idx}")
                entry["institution"] = st.text_input("Institution", value=entry["institution"], key=f"institution_{idx}")
            with col2:
                entry["start"] = st.text_input("Start Year", value=entry["start"], key=f"start_{idx}")
                entry["end"] = st.text_input("End Year", value=entry["end"], key=f"end_{idx}")
            entry["grade"] = st.text_input("Grade/Percentage", value=entry["grade"], key=f"grade_{idx}")

def experience_section():
    st.subheader("💼 Work Experience")
    return st.text_area("Describe your work experience with bullet points (\\n-separated)", key="experience", height=120,
                       placeholder="• Led a team of 5 developers to deliver a customer portal application\n• Implemented RESTful APIs using Node.js and Express\n• Reduced application load time by 40% through optimization\n• Managed database design and deployment on AWS")

def project_section():
    st.subheader("🚀 Projects")
    # Project title and description in a more organized layout
    title = st.text_input("Project Title", key="project_title", placeholder="e.g., E-commerce Website, Machine Learning Model")
    desc = st.text_area("Project Description (\\n-separated for bullet points)", key="project_desc", height=120, 
                       placeholder="• Developed a full-stack web application using React and Node.js\n• Implemented user authentication and payment processing\n• Deployed on AWS with CI/CD pipeline")
    return title, desc

def skills_section():
    st.subheader("🧠 Skills")
    return st.text_input("List your skills (comma separated)", key="skills", placeholder="e.g., Python, JavaScript, Machine Learning, Project Management")

def additional_sections():
    st.subheader("📌 Additional Sections (Optional)")
    # Use columns for better layout
    col1, col2 = st.columns(2)
    with col1:
        volunteering = st.text_area("Volunteering / Extra-curricular Activities", key="volunteering", height=100)
        certifications = st.text_area("Certifications / Courses", key="certifications", height=100)
    with col2:
        hobbies = st.text_input("Hobbies (comma separated)", key="hobbies", placeholder="e.g., Reading, Hiking, Photography")
    return volunteering, hobbies, certifications
