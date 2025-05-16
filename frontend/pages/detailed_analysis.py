import streamlit as st

st.set_page_config(page_title="Detailed Analysis", page_icon="📊")

# Check if the analysis result is in the session state
if 'analysis_result' in st.session_state:
    result = st.session_state['analysis_result']

    st.title("Detailed Resume Analysis")
    st.markdown("---")

    st.markdown(f"### ✅ Resume Score: `{result.get('score', 'N/A')}/100`")

    st.markdown("### 🎯 Field of Interest:")
    st.markdown(f"`{result.get('field_of_interest', 'N/A')}`")

    st.markdown("### 💡 Suggestions:")
    suggestions = result.get("suggestions", [])
    if suggestions:
        for i, suggestion in enumerate(suggestions, 1):
            st.markdown(f"{i}. {suggestion}")
    else:
        st.markdown("No specific suggestions found.")

    st.markdown("### 🧐 Detailed Analysis:")
    detailed_analysis = result.get('detailed_analysis', {})
    if detailed_analysis:
        st.markdown(f"**Overall Assessment:** {detailed_analysis.get('overall_assessment', 'N/A')}")

        st.markdown("#### Strengths:")
        strengths = detailed_analysis.get('strengths', [])
        if strengths:
            for strength in strengths:
                st.markdown(f"- {strength}")
        else:
            st.markdown("No strengths identified.")

        st.markdown("#### Weaknesses:")
        weaknesses = detailed_analysis.get('weaknesses', [])
        if weaknesses:
            for weakness in weaknesses:
                st.markdown(f"- {weakness}")
        else:
            st.markdown("No weaknesses identified.")

        st.markdown("#### Reasoning for Field of Interest:")
        st.markdown(detailed_analysis.get('reasoning_for_field', 'N/A'))
    else:
        st.markdown("No detailed analysis available.")
else:
    st.warning("Please upload your resume and enter a job title on the main page to see the detailed analysis.")