import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "..", "data", "syllabus", "sem4_syllabus.json")

def syllabus_tool(query: str):
    with open(DATA_PATH, "r") as f:
        data = json.load(f)

    q = query.lower()
    subjects = data.get("subjects", [])

    # List subjects
    if any(k in q for k in ["subjects", "courses", "papers"]):
        names = [f"{s['code']} – {s['name']}" for s in subjects]
        return "Semester 4 subjects:\n" + "\n".join(names)

    # Match subject by code or name
    for s in subjects:
        if s["code"].lower() in q or s["name"].lower() in q:
            response = f"**{s['code']} – {s['name']}**\n"
            response += f"Credits: {s['credits']}\n\n"

            if "objective" in q:
                response += "Course Objectives:\n"
                response += "\n".join(f"- {o}" for o in s["objectives"])
                return response

            if "outcome" in q:
                response += "Course Outcomes:\n"
                response += "\n".join(f"- {o}" for o in s["outcomes"])
                return response

            if "syllabus" in q or "topics" in q:
                response += "Syllabus:\n"
                response += "\n".join(f"- {t}" for t in s["syllabus"])
                return response

            return response

    return "I couldn’t find a matching Semester 4 subject for your query."
