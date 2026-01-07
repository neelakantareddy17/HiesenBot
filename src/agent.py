import os
from dotenv import load_dotenv
load_dotenv()

import google.generativeai as genai

from src.tools.mess_tool import mess_menu_tool
from src.tools.academic_tool import academic_tool
from src.tools.syllabus_tool import syllabus_tool


def build_agent():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY is missing!")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-flash-latest")

    def agent_executor(query: str):
        q = query.lower()

        # 1. Mess-related queries (highest priority)
        if any(d in q for d in [
            "monday", "tuesday", "wednesday",
            "thursday", "friday", "saturday", "sunday",
            "breakfast", "lunch", "dinner", "snacks", "mess"
        ]):
            return mess_menu_tool(query)

        # 2. Syllabus-related queries
        if any(k in q for k in [
            "syllabus", "subject", "subjects", "course",
            "courses", "topics", "unit", "units", "semester 4", "sem 4"
        ]):
            return syllabus_tool(query)

        # 3. Academic calendar / exam queries
        if any(k in q for k in [
            "holiday", "exam", "mid", "endsem",
            "class", "start", "begin", "calendar", "attendance"
        ]):
            return academic_tool(query)

        # 4. Fallback to LLM
        response = model.generate_content(query)
        return response.text

    return agent_executor
