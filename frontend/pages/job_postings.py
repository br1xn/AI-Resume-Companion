# frontend/pages/job_postings.py (remains as provided in previous response)
import streamlit as st
import requests
import pandas as pd
import os

st.set_page_config(page_title="Job Postings", page_icon="🔍")

FASTAPI_BASE_URL = os.getenv("FASTAPI_BASE_URL", "http://localhost:8000")

st.title("🔍Find Jobs Based on Your Resume")
st.markdown("---")

analysis_result = st.session_state.get('analysis_result', None)
field_of_interest = st.session_state.get('interest', None)

if analysis_result and field_of_interest:
    st.write(f"Searching jobs for: **{field_of_interest}**")
    location = st.text_input("Preferred Location", value="India")

    if st.button("Find Jobs"):
        with st.spinner("Fetching job postings..."):
            try:
                extracted_keywords = analysis_result.get('keywords', [])

                # This is the call that goes to your FastAPI backend
                job_search_data = {
                    "job_title": field_of_interest,
                    "location": location,
                    "keywords": extracted_keywords
                }
                # It calls the `get_job_postings_api` endpoint in your backend/main.py
                response = requests.post(f"{FASTAPI_BASE_URL}/get_job_postings", json=job_search_data)

                if response.status_code == 200:
                    linkedin_jobs = response.json()
                    if linkedin_jobs:
                        st.success(f"Found {len(linkedin_jobs)} job postings related to '{field_of_interest}'. Displaying top {min(len(linkedin_jobs), 10)}...")
                        top_jobs = linkedin_jobs[:10]

                        data = {
                            "Job Title": [job["title"] for job in top_jobs],
                            "Company": [job["company"] for job in top_jobs],
                            "Location": [job["location"] for job in top_jobs],
                            "Apply Link": [f'<a href="{job["url"]}" target="_blank">Click Here</a>' for job in top_jobs],
                        }
                        df = pd.DataFrame(data)
                        st.markdown(df.to_markdown(index=False), unsafe_allow_html=True)
                    else:
                        st.warning("No relevant jobs found.")
                else:
                    st.error(f"Failed to fetch job postings from backend. Status: {response.status_code}, Error: {response.text}")
            except requests.exceptions.ConnectionError:
                st.error("Could not connect to the backend service. Please ensure it's running and accessible.")
            except Exception as e:
                st.error(f"An unexpected error occurred while fetching jobs: {e}")
                st.info("Please ensure your backend is running and accessible and your `requirements.txt` are complete.")
else:
    st.warning("Please analyze your resume on the main page first to search for jobs.")

st.markdown("---")
if st.button("Go back to Main Analysis"):
    st.switch_page("app.py")