import google.generativeai as genai
import os
from dotenv import load_dotenv
import json  
import re

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY") 
genai.configure(api_key=API_KEY)

# Initialize Gemini model
model = genai.GenerativeModel("gemini-2.0-flash")

def analyze_resume_with_gemini(resume_text: str, job_title: str) -> dict:
    prompt = f"""
    Analyze the following resume for the job title: {job_title}.

    Provide a detailed analysis in JSON format, considering how well the resume is tailored to this specific job title.

    The JSON object should contain the following keys:
    - "score": An integer representing the resume score from 0 to 100, specifically for the given job title.
    - "suggestions": A list of three specific and actionable suggestions for improvement, tailored to the job title.
    - "field_of_interest": A string representing the candidate's primary field of interest inferred from the resume content.
    - "detailed_analysis": A dictionary with the following keys:
        - "overall_assessment": A string providing an overall assessment of the resume's suitability for the job title.
        - "strengths": A list of strings highlighting the resume's strengths in relation to the job title.
        - "weaknesses": A list of strings pointing out the resume's weaknesses in relation to the job title.
        - "reasoning_for_field": A string explaining the reasoning behind the inferred field of interest.

    Example JSON response:
    {{
      "score": 68,
      "suggestions": ["Highlight project experience relevant to {job_title}.", "Quantify achievements with metrics related to {job_title}.", "Customize the skills section for {job_title}."],
      "field_of_interest": "Software Engineering",
      "detailed_analysis": {{
        "overall_assessment": "The resume shows some potential for a {job_title} role, but needs better tailoring.",
        "strengths": ["Strong technical skills are mentioned.", "Education is relevant to {job_title}."],
        "weaknesses": ["Lack of specific {job_title} experience is evident.", "Achievements are not quantified in a {job_title} context.", "Resume is generic, not targeted."],
        "reasoning_for_field": "The resume emphasizes programming skills and software development projects."
      }}
    }}

    Resume:
    \"\"\"
    {resume_text}
    \"\"\"

    Respond ONLY with the JSON object. Do not include any other text or explanations, including Markdown code blocks.
    """

    try:
        response = model.generate_content([prompt])
        if response.parts and hasattr(response.parts[0], "text"):
            raw_text = response.parts[0].text.strip()  # Remove leading/trailing whitespace
            # Remove Markdown code block markers if present
            json_string = re.sub(r'```json\n?', '', raw_text)
            json_string = re.sub(r'```', '', json_string).strip()

            try:
                # Attempt to load the JSON response
                json_output = json.loads(json_string)
                return json_output
            except json.JSONDecodeError as e:
                print(f"JSON Decode Error: {e}")
                print(f"Raw Gemini Response: {raw_text}")
                print(f"Processed JSON String: {json_string}")
                return {
                    "score": 50,
                    "suggestions": ["Gemini's response was not in the expected JSON format."],
                    "field_of_interest": "Unknown"
                }
        else:
            return {
                "score": 50,
                "suggestions": ["No response text received from Gemini."],
                "field_of_interest": "Unknown"
            }
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return {
            "score": 30,
            "suggestions": [f"An error occurred while calling the Gemini API: {e}"],
            "field_of_interest": "Error"
        }
    
# For roadmap
def generate_roadmap_with_gemini(field_of_interest: str) -> dict:
    """
    Generates a roadmap of tutorials, certifications, and projects for a given field
    of interest using the Gemini model.
    """
    prompt = f"""
    Generate a comprehensive career roadmap for someone entering or advancing in the field of "{field_of_interest}".
    Focus on practical, actionable steps and provide direct, reputable links for resources.

    The roadmap should include:

    -   **Tutorials:** Suggest 3-5 high-quality online tutorials or courses. For each, provide:
        -   `title`: The name of the tutorial/course.
        -   `link`: A direct URL to the resource.
        -   `platform`: The hosting platform (e.g., YouTube, Coursera, freeCodeCamp).
        -   `description`: A brief summary of what the tutorial covers.

    -   **Certifications:** Recommend 2-4 widely recognized industry certifications. For each, provide:
        -   `title`: The name of the certification.
        -   `link`: A direct URL to the certification's official page.
        -   `provider`: The certifying body (e.g., CompTIA, ISC2, Google).
        -   `description`: A brief explanation of the certification's value.

    -   **Projects:** Propose 3-5 practical project ideas. For each, provide:
        -   `title`: A clear, concise project name.
        -   `description`: A short explanation of what the project entails and its learning objectives.
        -   `difficulty`: "Beginner", "Intermediate", or "Advanced".

    Ensure all provided links are valid and lead directly to the suggested resource. Prioritize resources from well-known educational platforms, industry associations, or reputable companies.

    The response *must* be in JSON format, with the following exact structure:

    ```json
    {{
        "tutorials": [
            {{"title": "Tutorial Title", "link": "[https://example.com/tutorial](https://example.com/tutorial)", "platform": "Platform Name", "description": "Brief description of the tutorial."}},
            // ... more tutorials
        ],
        "certifications": [
            {{"title": "Certification Title", "link": "[https://example.com/cert](https://example.com/cert)", "provider": "Provider Name", "description": "Brief description of the certification."}},
            // ... more certifications
        ],
        "projects": [
            {{"title": "Project Title", "description": "Brief description of the project.", "difficulty": "Difficulty Level"}},
            // ... more projects
        ]
    }}
    ```
    Respond ONLY with the JSON object. Do not include any other text or explanations, including Markdown code blocks.
    """

    try:
        response = model.generate_content([prompt])
        if response.parts and hasattr(response.parts[0], "text"):
            raw_text = response.parts[0].text.strip()
            json_string = re.sub(r'```json\n?', '', raw_text)
            json_string = re.sub(r'```', '', json_string).strip()

            try:
                roadmap_data = json.loads(json_string)
                return roadmap_data
            except json.JSONDecodeError as e:
                print(f"JSON Decode Error in generate_roadmap_with_gemini: {e}")
                print(f"Raw Gemini Response: {raw_text}")
                print(f"Processed JSON String: {json_string}")
                return {"error": "Invalid JSON response from Gemini for roadmap."}
        else:
            return {"error": "No response text received from Gemini for roadmap."}
    except Exception as e:
        print(f"Gemini API Error in generate_roadmap_with_gemini: {e}")
        return {"error": f"An error occurred while calling the Gemini API for roadmap: {e}"}