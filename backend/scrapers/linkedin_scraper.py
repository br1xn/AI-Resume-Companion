from typing import List, Dict
import httpx
from bs4 import BeautifulSoup
import asyncio

async def scrape_linkedin(job_title:str, location: str, _, keywords: List[str]) -> List[Dict]:
    """
    Asynchronously scrapes job postings from LinkedIn, tailored to keywords.
    """
    job_title_encoded = job_title.replace(" ", "%20")
    location_encoded = location.replace(" ", "%20")
    keywords_encoded = "%20".join(keywords)
    url = f"https://www.linkedin.com/jobs/search/?keywords={job_title_encoded}%20{keywords_encoded}&location={location_encoded}" # Removed &level={job_level}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            job_listings = soup.find_all('div', class_='base-card')
            jobs = []
            for job in job_listings:
                title = job.find('h3', class_='base-search-card__title').text.strip() if job.find('h3', class_='base-search-card__title') else "N/A"
                company = job.find('h4', class_='base-search-card__subtitle').text.strip() if job.find('h4', class_='base-search-card__subtitle') else "N/A"
                location_element = job.find('span', class_='job-search-card__location').text.strip() if job.find('span', class_='job-search-card__location') else "N/A"
                link_element = job.find('a')
                link = link_element['href'] if link_element and 'href' in link_element.attrs else "#"

                jobs.append({
                    'title': title,
                    'company': company,
                    'location': location_element,
                    'url': link,
                    'source': 'linkedin'
                })
            return jobs
    except httpx.RequestError as e:
        print(f"Error fetching LinkedIn jobs: {e}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []