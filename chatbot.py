
import requests
import pandas as pd

HUGGINGFACE_API_KEY = "yourapi"
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"

headers = {
    "Authorization": f"Bearer {HUGGINGFACE_API_KEY}"
}

# Load Class Schedule once
class_schedule_df = pd.read_excel("CLASS_SCHEDULE_4764.xlsx")


def query_huggingface(prompt):
    payload = {
        "inputs": prompt,
        "options": {"wait_for_model": True}
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()[0]['generated_text']


def check_elective_availability(recommended_courses):
    current_term = 2403
    offered_courses = class_schedule_df[class_schedule_df['Term'] == current_term]['Descr'].unique().tolist()
    available = []
    unavailable = []
    for course in recommended_courses:
        if any(course.lower() in offered.lower() for offered in offered_courses):
            available.append(course)
        else:
            unavailable.append(course)
    return available, unavailable


def build_prompt(student_context, user_question):
    return f"""
Instruction: You are a student advisory assistant. Based on the academic record below, answer the student's question clearly and helpfully.

Academic Record:
{student_context}

Question:
{user_question}

Answer:"""


def final_advisory_response(student_context, user_question, raw_response):
    # Extract recommended courses from the raw_response (basic rule-based parse)
    suggested = []
    keywords = ["Operations Management", "Data Analytics", "Machine Learning", "Entrepreneurship",
                "Supply Chain Management", "International Business"]
    for kw in keywords:
        if kw.lower() in raw_response.lower():
            suggested.append(kw)

    available, unavailable = check_elective_availability(suggested)

    final_output = raw_response.strip()
    final_output += "\n\n📌 **Elective Availability Check (Term 2403):**"
    if available:
        final_output += f"\n✅ Available: {', '.join(available)}"
    if unavailable:
        final_output += f"\n❌ Not Available: {', '.join(unavailable)}"

    final_output += "\n\n🎓 **Final Advisory Conclusion:** Based on your academic strengths and the current term offerings, you are encouraged to register for the available electives listed above. For unavailable courses, consider them in future terms. Good luck!"

    return final_output
