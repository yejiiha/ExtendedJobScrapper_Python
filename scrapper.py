import requests
from bs4 import BeautifulSoup

def get_last_page(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")

    pages = soup.find("div", {"class": "s-pagination"}).find_all("a")
    last_page = pages[-2].get_text(strip=True)

    return int(last_page)


def extract_job(html):
    #extract title
    title = html.find("h2").text.strip()
    #extract company and location
    company_row = html.find("h3", {
        "class": "fs-body1"
    }).find_all(
        "span", recursive=False)
    #company_row has 2 spans
    company = company_row[0].get_text(strip=True)
    location = company_row[1].get_text(strip=True)
    #extract apply link
    job_id = html['data-jobid']
    
    return {
        'title': title,
        'company': company,
        'location': location,
        'link': f"https://stackoverflow.com/jobs/{job_id}"
    }


def extract_jobs(last_page, url):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping SO page {page}")
        result = requests.get(f"{url}&pg={page+1}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "-job"})

        for result in results:
            job = extract_job(result)
            jobs.append(job)

    return jobs


def get_jobs(word):
    #construct url with word we sent
    url = f"https://stackoverflow.com/jobs?q={word}"
    last_page = get_last_page(url)
    jobs = extract_jobs(last_page, url)

    return jobs
