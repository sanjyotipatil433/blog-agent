from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

def brainstorm_titles(state: dict) -> dict:
    prompt = f"""You are a blog title expert.
Context: {state['context']}

Generate 5 compelling blog titles as a numbered list like:
1. Title one
2. Title two
3. Title three
4. Title four
5. Title five"""

    response = llm.invoke(prompt)
    
    lines = response.content.strip().split("\n")
    titles = [line.split(". ", 1)[1] for line in lines 
              if line.strip() and line[0].isdigit()]
    
    return {
        "title_candidates": titles,
        "chosen_title": titles[0]
    }