import streamlit as st
import requests
import os

st.set_page_config(page_title="Career Guide", page_icon="📄", layout="centered")

st.title("📄 Career Guidance Assistant")
st.subheader("Upload your resume to get feedback, suggestions, and tailored career insights")

# URL
FASTAPI_BASE_URL = os.getenv("FASTAPI_BASE_URL", "http://localhost:8000")

# Upload Resume & set Job Title
uploaded_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"])
job_title = st.text_input("Enter your preferrred job title:", "")

if uploaded_file and job_title:
    with st.spinner("Analyzing your resume..."):
        files = {"resume": uploaded_file}  # Pass the uploaded file object directly
        data = {"job_title": job_title}

        response = requests.post("{FASTAPI_BASE_URL}/analyze_resume", files=files, data=data)

    if response.status_code == 200:
        try:
            result = response.json()
            st.success("Analysis complete!")

            # Storing results for detailed analysis page
            st.session_state['analysis_result'] = result
            st.session_state['uploaded_file'] = uploaded_file

            # Display results
            st.markdown(f"### ✅ Resume Score: `{result.get('score', 'N/A')}/100`")
            st.markdown("### 💡 Suggestions:")
            suggestions = result.get("suggestions", [])
            if suggestions:
                for i, suggestion in enumerate(suggestions, 1):
                    st.markdown(f"{i}. {suggestion}")
            else:
                st.markdown("No specific suggestions found.")

            st.markdown(f"### 🎯 Field of Interest: `{result.get('field_of_interest', 'N/A')}`")

            # Action options
            st.markdown("---")
            st.markdown("### What would you like to do next?")

            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("🔍 See Job Postings"):
                    st.switch_page("pages/job_postings.py")

            with col2:
                if st.button("🛠️ Build My Roadmap"):
                    st.session_state['interest'] = result.get("field_of_interest", "")
                    st.switch_page("pages/roadmap.py")
            with col3:
                if st.button("🧐 Detailed Analysis"):
                    st.switch_page("pages/detailed_analysis.py")

        except Exception as e:
            st.error(f"Error processing the analysis result: {e}")
            st.error(f"Raw response: {response.text}") # For debugging
    else:
        st.error(f"Something went wrong. Please try again. Status code: {response.status_code}")
        st.error(f"Response text: {response.text}")
elif uploaded_file and not job_title:
    st.warning("Please enter a job title to analyze your resume.")
elif job_title and not uploaded_file:
    st.warning("Please upload your resume to get it analyzed for the job title")