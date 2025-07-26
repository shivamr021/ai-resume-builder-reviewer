import streamlit as st
from builder.form_handler import handle_resume_form
from builder.styles import load_css
from reviewer.resume_parser import extract_text_from_pdf
from reviewer.ats_scoring import calculate_ats_score
from insights.suggestions import extract_section_wise_keywords

st.set_page_config(page_title="AI Resume Reviewer", layout="wide")

# Load custom CSS styles
load_css()

tab1, tab2, tab3 = st.tabs(["📝 Build Resume", "📊 ATS Review", "🧠 Suggestions"])

# ------------------ Tab 1 ------------------
with tab1:
    st.header("Resume Builder")
    st.write("Fill out your details to generate a professional resume.")
    handle_resume_form()

# ------------------ Tab 2 ------------------
with tab2:
    st.header("📊 ATS Score Review")
    st.write("Upload your resume and optionally paste a job description to evaluate your ATS compatibility.")

    uploaded_resume = st.file_uploader("📄 Upload Your Resume (PDF)", type=["pdf"], key="resume_tab2")
    job_description = st.text_area("📝 Paste the Job Description (Optional)", height=200)

    if st.button("🔍 Analyze Resume", key="score_button"):
        if uploaded_resume:
            try:
                resume_text = extract_text_from_pdf(uploaded_resume)
                ats_result = calculate_ats_score(resume_text, job_description)

                st.subheader("🎯 ATS Match Score")
                st.success(f"Score: {ats_result['score']} / 100")
                st.progress(int(ats_result['score']))

                if ats_result['fallback_mode']:
                    st.info("ℹ️ No job description provided. Score is based on keyword richness.")
                    st.markdown("**🧠 Resume Keywords Extracted:**")
                    st.write(", ".join(ats_result['resume_keywords']))

            except Exception as e:
                st.error(f"❗ Error processing resume: {e}")
        else:
            st.warning("⚠️ Please upload a resume to begin analysis.")

# ------------------ Tab 3 ------------------
with tab3:
    st.header("🧠 Resume Improvement Suggestions")
    st.write("This section analyzes your resume for relevant keywords and offers actionable feedback.")

    if uploaded_resume:
        try:
            resume_text = extract_text_from_pdf(uploaded_resume)
            found_kw, missing_kw = extract_section_wise_keywords(resume_text)

            st.markdown("### ✅ Keywords Found (Grouped by Section)")
            for section, keywords in found_kw.items():
                if keywords:
                    with st.expander(f"🔹 {section}", expanded=False):
                        st.markdown(f"`{', '.join(keywords)}`")

            st.markdown("### ❌ Keywords Missing (Consider Adding These)")
            for section, keywords in missing_kw.items():
                if keywords:
                    with st.expander(f"🔸 {section}", expanded=False):
                        for kw in keywords:
                            st.markdown(f"- *Consider adding `{kw}` to your {section} section.*")

        except Exception as e:
            st.error(f"Error analyzing resume: {e}")
    else:
        st.warning("Upload a resume in Tab 2 to get suggestions here.")
