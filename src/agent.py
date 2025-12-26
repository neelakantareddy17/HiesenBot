import os
from dotenv import load_dotenv
load_dotenv()

import google.generativeai as genai
from src.tools.mess_tool import mess_menu_tool
from src.tools.academic_tool import academic_tool


def build_agent():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY is missing!")

    genai.configure(api_key=api_key)

    # Use a VALID model from your account
    model = genai.GenerativeModel("gemini-flash-latest")

    def agent_executor(query: str):
        q = query.lower()

        if any(d in q for d in ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]) \
           or any(m in q for m in ["breakfast","lunch","dinner","snacks"]):
            return mess_menu_tool(query)

        if any(k in q for k in ["holiday","exam","mid","endsem","class","start","begin","calendar"]):
            return academic_tool(query)

        response = model.generate_content(query)
        return response.text

    return agent_executor
