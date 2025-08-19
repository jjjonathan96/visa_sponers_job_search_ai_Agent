import streamlit as st
from scraper import scrape_jobs
from filter_agent import filter_relevant_jobs
from db import save_jobs, get_all_jobs, mark_job_as_applied

# --- Global Settings ---
keyword = ['machine learning', 'ai', 'llm', 'rag', 'deep learning']
user_pref = st.text_input("Your job preferences (e.g., UK-based, remote, LLM)")
filtered_jobs = []

# --- Page Selector ---
page = st.sidebar.selectbox("Choose a page", ["🏠 Home", "🔍 Job Search", "🧩 CV Tailoring"])

# ---------------- Home Page ----------------
if page == "🏠 Home":
    st.title("Welcome to JJ Job AI Agent 👋")
    st.write("Use the sidebar to navigate between job search and CV tailoring.")
    st.subheader("🗂️ Saved Jobs")

    jobs = get_all_jobs()

    show_only_unapplied = st.checkbox("Show only unapplied jobs", value=True)
    if show_only_unapplied:
        jobs = [job for job in jobs if not job.get("applied", False)]

    if not jobs:
        st.info("No saved jobs found.")
    else:
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
                        st.rerun()

# ---------------- Job Search Page ----------------
elif page == "🔍 Job Search":
    st.title("Job Search")
    selected_page = st.selectbox("Select job page to scrape", ['nhs','adzuna', 'dwp', 'linked in','indeed', 'cv library','glass door'])

    if st.button("Scrape Jobs"):
        value = 1
        for page_num in range(value, 3):  # reduce pages for faster testing
            linked_dict = {
                'nhs':'https://www.healthjobsuk.com/job_list/ns?JobSearch_q=data+science&JobSearch_QueryIntegratedSubmit=Search&_tr=JobSearch&_ts=1',
                'findajobdwp':'https://findajob.dwp.gov.uk/search?loc=86383&pp=25&q=machine%20learning%20engineer',
                'gradecracker':'https://www.gradcracker.com/keyword-search?query=machine+learning&degree-apprenticeships=1&placements=1&jobs=1',
                'adzuna':f'https://www.adzuna.co.uk/jobs/search?loc=86383&st=45000&q=Machine%20Learning%20Engineer&p={page_num}', 
                'dwp':f'https://findajob.dwp.gov.uk/search?loc=86383&p={page_num-1}&q=machine%20learning', 
                'linked in':f'https://www.linkedin.com/jobs/search/?currentJobId=4267176685&distance=25&f_E=2&f_PP=108541532%2C104006709%2C100356971%2C103615590%2C102681496%2C100209086%2C104097054%2C104599251%2C102943586%2C106611729%2C104470941%2C112709004&geoId=101165590&keywords=machine%20learning&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&sortBy=R&start={page_num*25}',
                'linkedin':'https://www.linkedin.com/jobs/search/?currentJobId=4265031640&distance=25&f_E=2&f_PP=108541532%2C103615590%2C100209086%2C104006709%2C102681496%2C100925589%2C101915881%2C103024982%2C106611729%2C104097054%2C104599251%2C102943586%2C100080230&geoId=101165590&keywords=machine%20learning%20engineer&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&sortBy=R&start=25',
                'indeed':'', 
                'cv library':'',
                'glass door':''
            }

            url = linked_dict[selected_page]
            if not url:
                st.warning(f"No scraping logic yet for {selected_page}")
                break

            st.write(f"🔗 Scraping: {url}")
            with st.spinner("Scraping jobs..."):
                jobs = scrape_jobs(url, keyword)

            if jobs:
                save_jobs(jobs)
                st.success(f"✅ {len(jobs)} jobs scraped and saved.")

                with st.spinner("Filtering best matches using OpenAI..."):
                    for i in range(0, len(jobs), 5):
                        filtered = filter_relevant_jobs(jobs[i:i+5], user_pref)
                        filtered_jobs.extend(filtered)

                st.subheader("🎯 Top AI-filtered Jobs (Unapplied)")
                for job in filtered_jobs:
                    if not job.get("applied"):
                        with st.expander(f"{job['title']}"):
                            st.write(f"📍 Location: {job.get('location', 'N/A')}")
                            st.write(f"🔗 [View Job]({job['link']})")
                            st.write(f"📝 Summary: {job.get('description', 'N/A')[:300]}...")

# ---------------- CV Tailoring Page ----------------
elif page == "🧩 CV Tailoring":
    st.title("CV Tailoring")

    saved_jobs = get_all_jobs()
    unapplied_jobs = [j for j in saved_jobs if not j.get("applied")]

    if not unapplied_jobs:
        st.warning("Please run job search first or no unapplied jobs found.")
    else:
        selected_job = st.selectbox("Select a job to tailor CV for", [
            f"{j['title']} - {j['link']}" for j in unapplied_jobs])
        st.text_area("Paste your general CV here:")
        st.button("Tailor My CV")
