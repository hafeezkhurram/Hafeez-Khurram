import requests
from bs4 import BeautifulSoup
import json
import time
import random

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

def scrape_linkedin(keyword="data analyst" , max_jobs=100):
    jobs = []
    url_template = "https://www.linkedin.com/jobs/search?keywords={}&start={}"
    start = 0

    while len(jobs) < max_jobs:
        url = url_template.format(keyword.replace(" ", "%20"), start)
        print(f"Scraping LinkedIn: {url}")
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(f"Failed to fetch page: Status {response.status_code}")
            break

        soup = BeautifulSoup(response.text, "html.parser")
        
        # Job cards
        job_cards = soup.find_all("div", class_="base-card")

        if not job_cards:
            print("No job cards found, maybe LinkedIn blocked the request or changed the layout.")
            break

        for card in job_cards:
            title_tag = card.find("h3", class_="base-search-card__title")
            company_tag = card.find("h4", class_="base-search-card__subtitle")
            location_tag = card.find("span", class_="job-search-card__location")

            title = title_tag.text.strip() if title_tag else None
            company = company_tag.text.strip() if company_tag else None
            location = location_tag.text.strip() if location_tag else None

            job = {
                "source": "LinkedIn",
                "title": title,
                "company": company,
                "location": location,
                "skills": [],  # Skills extraction not possible directly here
                "date_posted": None  # No easy access without JS rendering
            }
            jobs.append(job)
            if len(jobs) >= max_jobs:
                break

        start += 25  # LinkedIn paginates by 25 jobs per page
        time.sleep(random.uniform(2, 4))

    return jobs

def main():
    keyword = "data analyst"
    linkedin_jobs = scrape_linkedin(keyword, max_jobs=100)

    with open("linkedin_jobs.json", "w", encoding="utf-8") as f:
        json.dump(linkedin_jobs, f, ensure_ascii=False, indent=4)

    print(f"Scraped {len(linkedin_jobs)} jobs and saved to linkedin_jobs.json")

if __name__ == "__main__":
    main()
