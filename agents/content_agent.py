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
    tone = state.get("tone", "formal")

    if length == "short":
        word_count = "200-300 words"
        sections = "Introduction and Conclusion only"
    else:
        word_count = "500-800 words"
        sections = "Introduction, 3-4 sections with subheadings, Conclusion"

    tone_instructions = {
        "formal": "Use professional, academic language. Be authoritative and structured. No jokes.",
        "casual": "Write like texting a friend. Short sentences, simple words. Use 'you' a lot.",
        "funny": "Be EXTREMELY funny and witty. Use jokes, puns, sarcasm and funny analogies. Every paragraph must have at least one joke. Make the reader laugh out loud!",
        "inspirational": "Be deeply motivating. Use powerful words and emotional stories. Make the reader want to change their life right now!"
    }

    prompt = f"""You are an expert blog writer.
Title: {state['chosen_title']}
Topic: {state['context']}
Tone: {tone_instructions.get(tone, tone_instructions['formal'])}

Write a {length} blog post with:
- {sections}
- Exactly {word_count}
- Do NOT repeat the title inside the blog body
- Start directly with the introduction
- STRICTLY follow the tone instructions above"""

    response = llm.invoke(prompt)

    return {
        "blog_content": response.content,
        "final_output": response.content
    }