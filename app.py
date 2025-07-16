import streamlit as st
from scraper import scrape_jobs
from filter_agent import filter_relevant_jobs
from db import save_jobs, get_all_jobs, mark_job_as_applied


# Page selector
page = st.sidebar.selectbox("Choose a page", ["🏠 Home", "🔍 Job Search", "🧩 CV Tailoring"])
keyword = ['machine learning', 'ai', 'llm', 'rag', 'deep learning']
user_pref = st.text_input("Your job preferences (e.g., UK-based, remote, LLM)")
filter =  []

# ---------------- Home Page ----------------
if page == "🏠 Home":
    st.title("Welcome to JJ Job AI Agent 👋")
    st.write("Use the sidebar to navigate between job search and CV tailoring.")
    st.subheader("🗂️ Saved Jobs")

    jobs = get_all_jobs()
    for job in jobs:
        with st.expander(f"{job['title']}"):
            st.write(f"📍 Location: {job.get('location', 'N/A')}")
            st.write(f"🔗 [View Job]({job['link']})")
            st.write(f"📝 Summary: {job.get('description', 'N/A')[:300]}...")
            if job.get("applied"):
                st.success("✅ Applied")
            else:
                if st.button(f"Mark as Applied - {job['link']}", key=job['link']):
                    mark_job_as_applied(job['link'])
                    st.experimental_rerun()
    show_only_unapplied = st.checkbox("Show only unapplied jobs", value=True)
    if show_only_unapplied:
        jobs = [job for job in jobs if not job.get("applied", False)]
    # ---------------- Job Search Page ----------------
elif page == "🔍 Job Search":
    st.title("Job Search")

    selected_page = st.selectbox("Select job page to scrape", ['nhs','adzuna', 'dwp', 'linked in','indeed', 'cv library','glass door'])
    job_data = []

    if st.button("Scrape Jobs"):
        
        value = 1
    
        for page_num in range(value, 10):
            linked_dict = {
                    'nhs':'',
                    'adzuna':f'https://www.adzuna.co.uk/jobs/search?loc=86383&st=45000&q=Machine%20Learning%20Engineer&p={page_num}', 
                    'dwp':f'https://findajob.dwp.gov.uk/search?loc=86383&p={page_num-1}&q=machine%20learning', 
                    'linked in':f'https://www.linkedin.com/jobs/search/?currentJobId=4267176685&distance=25&f_E=2&f_PP=108541532%2C104006709%2C100356971%2C103615590%2C102681496%2C100209086%2C104097054%2C104599251%2C102943586%2C106611729%2C104470941%2C112709004&geoId=101165590&keywords=machine%20learning&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&sortBy=R&start={page_num*25}',
                    'indeed':'', 
                    'cv library':'',
                    'glass door':''
                }

            url = linked_dict[selected_page]
            st.write(f"Scraping: {url}")
            with st.spinner("Scraping jobs..."):
                jobs = scrape_jobs(url, keyword)
                print('len jobs', len(jobs))
            st.write(value,len(jobs))
            save_jobs(jobs)
            if jobs:
                st.subheader("🎯 Top AI-filtered Jobs")
                with st.spinner("Filtering best matches using OpenAI..."):
                    for i in range(0,len(jobs), 5):
                        print('i', i)
                        filtered = filter_relevant_jobs(jobs[i:i+5], user_pref)
                        filter.append(filtered)
                        
                        st.write(filtered)
            value += 1
                

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


# https://www.linkedin.com/jobs/search/?currentJobId=4250744899&distance=25&f_E=2&f_PP=108541532%2C104006709%2C100356971%2C103615590%2C102681496%2C100209086%2C104097054%2C104599251%2C102943586%2C106611729%2C104470941%2C112709004&geoId=101165590&keywords=machine%20learning&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&sortBy=R&start=25
# https://www.linkedin.com/jobs/search/?currentJobId=4267176685&distance=25&f_E=2&f_PP=108541532%2C104006709%2C100356971%2C103615590%2C102681496%2C100209086%2C104097054%2C104599251%2C102943586%2C106611729%2C104470941%2C112709004&geoId=101165590&keywords=machine%20learning&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&sortBy=R&start=50


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
