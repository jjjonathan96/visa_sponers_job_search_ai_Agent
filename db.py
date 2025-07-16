from pymongo import MongoClient
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGO_URI)
db = client["job_db"]
collection = db["jobs"]

def save_jobs(jobs):
    for job in jobs:
        if not collection.find_one({"link": job["link"]}):  # avoid duplicates by link
            job["applied"] = False
            collection.insert_one(job)

def get_all_jobs():
    return list(collection.find())

def mark_job_as_applied(link):
    collection.update_one({"link": link}, {"$set": {"applied": True}})
