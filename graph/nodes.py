from agents.title_agent import brainstorm_titles
from agents.content_agent import generate_content

def topic_input_node(state: dict) -> dict:
    # Why this node? 
    # Prepares the topic as context for agents
    return {
        "context": state["topic"]
    }

def title_node(state: dict) -> dict:
    # Calls title agent
    return brainstorm_titles(state)

def content_node(state: dict) -> dict:
    # Calls content agent
    return generate_content(state)