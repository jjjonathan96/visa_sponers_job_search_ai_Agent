import streamlit as st
from scraper import scrape_jobs
from filter_agent import filter_relevant_jobs

# Page selector
page = st.sidebar.selectbox("Choose a page", ["🏠 Home", "🔍 Job Search", "🧩 CV Tailoring"])
keyword = ['machine learning', 'ai', 'llm', 'rag', 'deep learning']
user_pref = st.text_input("Your job preferences (e.g., UK-based, remote, LLM)")
filter =  []

# ---------------- Home Page ----------------
if page == "🏠 Home":
    st.title("Welcome to JJ Job AI Agent 👋")
    st.write("Use the sidebar to navigate between job search and CV tailoring.")

# ---------------- Job Search Page ----------------
elif page == "🔍 Job Search":
    st.title("Job Search")

    selected_page = st.selectbox("Select job page to scrape", ['nhs','adzuna', 'dwp', 'linked in','indeed', 'cv library','glass door'])
    job_data = []

    if st.button("Scrape Jobs"):
        pressed = True
        value = 0
        while pressed:
            for page_num in range(value, 100):
                

                linked_dict = {
                    'nhs':'',
                    'adzuna':f'https://www.adzuna.co.uk/jobs/search?loc=86383&st=45000&q=Machine%20Learning%20Engineer&p={page_num}', 
                    'dwp':'', 
                    'linked in':'',
                    'indeed':'', 
                    'cv library':'',
                    'glass door':''
                }

                url = linked_dict[selected_page]
                st.write(f"Scraping: {url}")
                with st.spinner("Scraping jobs..."):
                    jobs = scrape_jobs(url, keyword)
                    if jobs:
                        with st.spinner("Filtering best matches using OpenAI..."):
                            for i in range(0,len(jobs), 5):
                                filtered = filter_relevant_jobs(jobs[i:i+5], user_pref)
                                filter.append(filtered)
                            st.subheader("🎯 Top AI-filtered Jobs")
                            st.markdown(filter)
                break
            pressed = False
            while not pressed:
                pressed = st.button("Next Page")
                if pressed:
                    value += 1
                    break
                

# ---------------- CV Tailoring Page ----------------
elif page == "🧩 CV Tailoring":
    st.title("CV Tailoring")
    if "job_data" not in st.session_state:
        st.warning("Please run job search first.")
    else:
        selected_job = st.selectbox("Select a job to tailor CV for", [
            f"{j['title']} - {j['link']}" for j in st.session_state["job_data"]
        ])

        st.text_area("Paste your general CV here:")
        st.button("Tailor My CV")

# import streamlit as st
# from scraper import scrape_jobs
# from filter_agent import filter_relevant_jobs

# st.title("🔎 AI Job Search Assistant")
# url = 'https://findajob.dwp.gov.uk/search?q=machine+learning&w=UK'
# # '''
# # https://findajob.dwp.gov.uk/search?loc=86383&p=1&q=machine%20learning
# # https://findajob.dwp.gov.uk/search?loc=86383&p=2&q=machine%20learning
# # https://findajob.dwp.gov.uk/search?loc=86383&p=3&q=machine%20learning


# # https://findajob.dwp.gov.uk/search?loc=86383&p=2&pp=50&q=machine%20learning

# # https://www.adzuna.co.uk/jobs/search?q=Machine+Learning+Engineer&loc=86383&st=45000#
# # https://www.adzuna.co.uk/jobs/search?loc=86383&st=45000&q=Machine%20Learning%20Engineer&p=2


# # https://www.linkedin.com/jobs/search/?currentJobId=4265116772&f_E=2&geoId=101165590&keywords=machine%20learning&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON&refresh=true
# # https://www.linkedin.com/jobs/search/?currentJobId=4265386029&f_E=2&geoId=101165590&keywords=machine%20learning&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON&refresh=true&start=25
# # https://www.linkedin.com/jobs/search/?currentJobId=4265687166&f_E=2&f_PP=108541532&geoId=101165590&keywords=machine%20learning&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&sortBy=R
# # https://www.linkedin.com/jobs/search/?currentJobId=4265661297&f_E=2&f_PP=108541532&geoId=101165590&keywords=machine%20learning&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&sortBy=R&start=25
# # https://www.linkedin.com/jobs/search/?currentJobId=4233271728&f_E=2&f_PP=108541532&geoId=101165590&keywords=machine%20learning&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&sortBy=R&start=50

# # '''
# #site = st.text_input("Enter job website (e.g., https://careers.microsoft.com)")
# #keyword = st.text_input("Job keyword (e.g., Data Scientist, LLM, Remote)")
# keyword = ['machine learning', 'ai', 'llm', 'rag', 'deep learning']
# user_pref = st.text_input("Your job preferences (e.g., UK-based, remote, LLM)")
# site = 'https://findajob.dwp.gov.uk/'
# if st.button("Search"):
#     with st.spinner("Scraping jobs..."):
#         jobs = scrape_jobs(site, keyword)

#     st.success(f"Found {len(jobs)} matching jobs.")
#     st.write(jobs)
#     filter = []
#     if jobs:
#         with st.spinner("Filtering best matches using OpenAI..."):
#             for i in range(0,len(jobs), 5):
#                 filtered = filter_relevant_jobs(jobs[i:i+5], user_pref)
#                 filter.append(filtered)
#             st.subheader("🎯 Top AI-filtered Jobs")
#             st.markdown(filter)
