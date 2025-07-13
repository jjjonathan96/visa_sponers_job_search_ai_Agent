import openai
import os
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def filter_relevant_jobs(jobs, user_pref):
    job_text = "\n".join([f"{j['title']} - {j['link']}" for j in jobs])

    prompt = f"""
    You are a job assistant. The user is looking for jobs with preferences: {user_pref}.
    From the following list, pick only the most relevant 5 jobs and summarize them.

    {job_text}
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response['choices'][0]['message']['content']
