from agents.title_agent import brainstorm_titles
from agents.content_agent import generate_content

def topic_input_node(state: dict) -> dict:
    return {
        "context": state["topic"]
    }

def title_node(state: dict) -> dict:
    return brainstorm_titles(state)

def content_node(state: dict) -> dict:
    return generate_content(state)