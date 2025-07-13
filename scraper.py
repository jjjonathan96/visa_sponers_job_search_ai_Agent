import requests
from bs4 import BeautifulSoup

def scrape_jobs(url, keyword):
    jobs = []
    for i in range(10):

        #url = f'https://findajob.dwp.gov.uk/search?loc=86383&p={i}&q=machine%20learning'
        url = f'https://findajob.dwp.gov.uk/search?loc=86383&p={i}&pp=25&q=machine%20learning'
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')
        for a in soup.find_all('a', href=True):
            text = a.get_text(strip=True)
            if keyword.lower() in text.lower():
                jobs.append({'title': text, 'link': a['href']})
        
    return jobs
