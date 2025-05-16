from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from gemini_resume_analyzer import analyze_resume_with_gemini, generate_roadmap_with_gemini
import pdfplumber
from typing import Dict, List, Optional
from scrapers import linkedin_scraper

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def extract_text_from_pdf(file: UploadFile) -> str:
    try:
        with pdfplumber.open(file.file) as pdf:
            return "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
    except Exception as e:
        return f"Error reading PDF: {e}"

@app.post("/analyze_resume")
async def analyze_resume(resume: UploadFile = File(...), job_title: str = Form(...)) -> Dict:
    if resume.filename.endswith(".pdf"):
        resume_text = extract_text_from_pdf(resume)
    else:
        resume_text = (await resume.read()).decode("utf-8", errors="ignore")

    analysis_result = analyze_resume_with_gemini(resume_text, job_title)
    return analysis_result

async def get_job_postings_internal(job_title: str, location: str, keywords: List[str]) -> List[dict]:
    # Renamed this to avoid confusion with the endpoint function
    # This is the actual logic that calls your linkedin_scraper
    job_postings = []
    linkedin_jobs = await linkedin_scraper.scrape_linkedin(job_title, location, "", keywords)
    job_postings.extend(linkedin_jobs)
    return job_postings

# NOW, this is the FastAPI endpoint that your frontend will call:
@app.post("/get_job_postings") # <--- THIS IS THE ENDPOINT DECORATOR
async def get_job_postings_api(request_body: Dict) -> List[Dict]:
    """
    FastAPI endpoint to fetch job postings from the frontend.
    Expects 'job_title', 'location', and 'keywords' in the request body.
    """
    job_title = request_body.get("job_title")
    location = request_body.get("location")
    keywords = request_body.get("keywords", []) # Default to empty list if not provided

    if not job_title or not location:
        # Basic validation, consider returning a proper HTTP error
        return {"error": "Job title and location are required."} # FastAPI automatically handles 422 if Pydantic is used, but this is fine for now

    # Call your internal helper function that contains the scraping logic
    job_results = await get_job_postings_internal(job_title, location, keywords)
    return job_results

@app.post("/generate_roadmap")
async def generate_roadmap_endpoint(request_body: Dict) -> Dict:
    # FastAPI endpoint
    field_of_interest = request_body.get("field_of_interest")
    if not field_of_interest:
        return {"error": "Field of interest is required for roadmap generation."}

    # Call the new function from gemini_resume_analyzer
    roadmap_data = generate_roadmap_with_gemini(field_of_interest)
    return roadmap_data

