from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

def generate_content(state: dict) -> dict:
    length = state.get("blog_length", "long")
    
    if length == "short":
        word_count = "200-300 words"
        sections = "Introduction and Conclusion only"
    else:
        word_count = "500-800 words"
        sections = "Introduction, 3-4 sections with subheadings, Conclusion"

    prompt = f"""You are an expert blog writer.
Title: {state['chosen_title']}
Topic: {state['context']}

Write a {length} blog post with:
- {sections}
- Exactly {word_count}
- Do NOT repeat the title inside the blog body
- Start directly with the introduction"""

    response = llm.invoke(prompt)
    
    return {
        "blog_content": response.content,
        "final_output": response.content
    }