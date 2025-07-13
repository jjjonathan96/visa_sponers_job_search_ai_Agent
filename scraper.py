import requests
from bs4 import BeautifulSoup

def scrape_jobs(url, keyword):
    jobs = []
    url = 'https://findajob.dwp.gov.uk/search?loc=86383&p=1&q=machine%20learning'
    res = requests.get(url)
    print('res', res)
    soup = BeautifulSoup(res.text, 'html.parser')
    print('soup', soup)
    for a in soup.find_all('a', href=True):
        text = a.get_text(strip=True)
        if keyword.lower() in text.lower():
            jobs.append({'title': text, 'link': a['href']})
    
    return jobs
