# frontend/pages/roadmap.py
import streamlit as st
import requests
import os 

st.set_page_config(page_title="Career Roadmap", page_icon="🗺️")

st.title("🛠️ Your Personalized Roadmap")
st.markdown("---")


# URL 
FASTAPI_BASE_URL = os.getenv("FASTAPI_BASE_URL", "http://localhost:8000")


# Get field of interest from session state
field_of_interest = st.session_state.get('interest', None)

if field_of_interest:
    st.header(f"Your Roadmap for {field_of_interest}")
    st.markdown("Based on your resume, we've created a roadmap to help you achieve your career goals.")

    # Function to get roadmap suggestions from FastAPI
    def get_roadmap_suggestions(field: str):
        response = requests.post(f"{FASTAPI_BASE_URL}/generate_roadmap", json={"field_of_interest": field})
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to get roadmap suggestions: {response.text}")
            return None

    # Get roadmap suggestions from FastAPI
    # I recommend putting this inside a button to trigger it explicitly
    # This avoids making an API call every time the page loads if it's not needed.
    if st.button("Generate Roadmap"): # <-- Add a button here if you don't want it to generate automatically on page load
        with st.spinner("Generating personalized roadmap..."):
            roadmap_suggestions = get_roadmap_suggestions(field_of_interest)
            if roadmap_suggestions:
                st.session_state['roadmap_data'] = roadmap_suggestions # Store for persistence
            else:
                st.error("Could not generate roadmap. Please try again.")
    
    # Display generated roadmap if available in session state (after generation)
    if 'roadmap_data' in st.session_state and st.session_state['roadmap_data']:
        roadmap_data = st.session_state['roadmap_data']
        # Display Tutorials
        st.subheader("Recommended Tutorials")
        if "tutorials" in roadmap_data and roadmap_data["tutorials"]:
            for tutorial in roadmap_data["tutorials"]:
                link = tutorial.get('link', '#')
                platform = tutorial.get('platform', 'N/A')
                st.markdown(f"- [{tutorial['title']}]({link}) (Platform: {platform})")
        else:
            st.markdown("No tutorials found.")

        # Display Certifications
        st.subheader("Recommended Certifications")
        if "certifications" in roadmap_data and roadmap_data["certifications"]:
            for certification in roadmap_data["certifications"]:
                link = certification.get('link', '#')
                provider = certification.get('provider', 'N/A')
                st.markdown(f"- [{certification['title']}]({link}) (Provider: {provider})")
        else:
            st.markdown("No certifications found.")

        # Display Projects
        st.subheader("Recommended Projects")
        if "projects" in roadmap_data and roadmap_data["projects"]:
            for project in roadmap_data["projects"]:
                description = project.get('description', 'N/A')
                difficulty = project.get('difficulty', 'N/A')
                st.markdown(f"- **{project['title']}** (Difficulty: {difficulty})")
                st.markdown(f"  *Description*: {description}")
        else:
            st.markdown("No projects found.")
    else: 
        st.info("Click 'Generate Roadmap' to get your personalized career path!")


else:
    st.warning("Please upload your resume on the main page to get your personalized roadmap.")

st.markdown("---")
if st.button("Go back to Main Analysis"):
    st.switch_page("streamlit_app.py")