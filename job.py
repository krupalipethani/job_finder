from flask import Flask, render_template, request, jsonify
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "job_secret_key")

APP_ID = os.getenv("APP_ID")
APP_KEY = os.getenv("APP_KEY")


# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("index.html")


# ---------------- JOB SEARCH ----------------
@app.route("/search", methods=["POST"])
def search():

    skill = request.form.get("skill") or "python"
    location = request.form.get("location") or "India"
    salary_type = request.form.get("salary_type")

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
        return render_template("index.html", jobs=[])

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

    # ---------------- FILTERS ----------------
    filtered_jobs = []

    for job in jobs:

        job_location = (job.get("location") or "").lower()
        location_input = location.lower()

        # AREA FILTER (partial match)
        if location_input != "india":
            if location_input not in job_location:
                continue

        # SALARY FILTER
        salary = job.get("salary") or 0

        if salary_type == "low":
            if salary > 300000:
                continue

        elif salary_type == "mid":
            if salary < 300000 or salary > 800000:
                continue

        elif salary_type == "high":
            if salary < 800000:
                continue

        filtered_jobs.append(job)

    # fallback
    if not filtered_jobs:
        filtered_jobs = jobs

    return render_template("index.html", jobs=filtered_jobs)


# ---------------- SMART SUGGESTIONS ----------------
@app.route("/suggest")
def suggest():

    query = request.args.get("q", "").lower()

    suggestions_map = {
        "python": ["Python Developer", "Python Backend Developer", "Python Internship"],
        "java": ["Java Developer", "Java Spring Boot Developer"],
        "developer": ["Software Developer", "Frontend Developer", "Backend Developer"],
        "sales": ["Sales Executive", "Sales Manager"],
        "design": ["UI UX Designer", "Graphic Designer"],
        "data": ["Data Analyst", "Data Scientist"]
    }

    results = []

    for key in suggestions_map:
        if query in key:
            results.extend(suggestions_map[key])

    return jsonify({"suggestions": results[:5]})


# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(debug=True)