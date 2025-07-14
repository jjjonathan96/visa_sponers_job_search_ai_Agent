import requests
from bs4 import BeautifulSoup

def scrape_jobs(url, keywords):
    jobs = []
    for i in range(1,10):

        #url = f'https://findajob.dwp.gov.uk/search?loc=86383&p={i}&q=machine%20learning'
        #url = f'https://findajob.dwp.gov.uk/search?loc=86383&p={i}&pp=25&q=machine%20learning'
        url = f'https://www.linkedin.com/jobs/search/?currentJobId=4265661297&f_E=2&f_PP=108541532&geoId=101165590&keywords=machine%20learning&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&sortBy=R&start={i*25}'
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')
        for a in soup.find_all('a', href=True):
            text = a.get_text(strip=True)
            for keyword in keywords:
                if keyword.lower() in text.lower():
                    jobs.append({'title': text, 'link': a['href']})
        
    return jobs
