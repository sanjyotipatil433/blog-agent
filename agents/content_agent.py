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
    elif length == "medium":
        word_count = "400-500 words"
        sections = "Introduction, 2 sections with subheadings, Conclusion"
    else:
        word_count = "500-800 words"
        sections = "Introduction, 3-4 sections with subheadings, Conclusion"

    tone_instructions = {
        "formal": "Use sophisticated vocabulary, complex sentence structures and academic language. Sound like a Harvard professor.",
        "casual": "Write like you are texting a friend. Use very simple words, short sentences, contractions like don't/can't/won't. Feel warm and friendly.",
        "inspirational": "Be deeply emotional and motivating. Use powerful words, tell stories, make the reader feel they can change their life right now."
    }

    prompt = f"""You are an expert blog writer.
Title: {state['chosen_title']}
Topic: {state['context']}

TONE INSTRUCTION — this is the most important rule:
{tone_instructions.get(tone, tone_instructions['formal'])}

Write a {length} blog post with:
- {sections}
- Exactly {word_count}
- Do NOT repeat the title inside the blog body
- Start directly with the introduction
- STRICTLY follow the tone — the reader must immediately feel the difference"""

    response = llm.invoke(prompt)

    return {
        "blog_content": response.content,
        "final_output": response.content
    }