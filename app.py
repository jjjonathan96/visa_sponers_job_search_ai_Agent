import streamlit as st
from scraper import scrape_jobs
from filter_agent import filter_relevant_jobs

st.title("🔎 AI Job Search Assistant")
url = 'https://findajob.dwp.gov.uk/search?q=machine+learning&w=UK'
'''
https://findajob.dwp.gov.uk/search?loc=86383&p=1&q=machine%20learning
https://findajob.dwp.gov.uk/search?loc=86383&p=2&q=machine%20learning
https://findajob.dwp.gov.uk/search?loc=86383&p=3&q=machine%20learning


https://findajob.dwp.gov.uk/search?loc=86383&p=2&pp=50&q=machine%20learning
'''
#site = st.text_input("Enter job website (e.g., https://careers.microsoft.com)")
keyword = st.text_input("Job keyword (e.g., Data Scientist, LLM, Remote)")
user_pref = st.text_input("Your job preferences (e.g., UK-based, remote, LLM)")
site = 'https://findajob.dwp.gov.uk/'
if st.button("Search"):
    with st.spinner("Scraping jobs..."):
        jobs = scrape_jobs(site, keyword)

    st.success(f"Found {len(jobs)} matching jobs.")
    st.write(jobs)

    if jobs:
        with st.spinner("Filtering best matches using OpenAI..."):
            filtered = filter_relevant_jobs(jobs, user_pref)
            st.subheader("🎯 Top AI-filtered Jobs")
            st.markdown(filtered)
