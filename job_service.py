import os
import requests
from dotenv import load_dotenv

load_dotenv()

APP_ID = os.getenv("APP_ID")
APP_KEY = os.getenv("APP_KEY")


def find_jobs(skill, location="India"):

    url = "https://api.adzuna.com/v1/api/jobs/in/search/1"

    params = {
        "app_id": APP_ID,
        "app_key": APP_KEY,
        "what": skill,
        "where": location,
        "results_per_page": 20
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        return []

    data = response.json()

    jobs = []

    for job in data.get("results", []):

        jobs.append({
            "title": job.get("title"),
            "company": job.get("company", {}).get("display_name"),
            "location": job.get("location", {}).get("display_name"),
            "salary": job.get("salary_min") or 0,
            "url": job.get("redirect_url")
        })

    return jobs