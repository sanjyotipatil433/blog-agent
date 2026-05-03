from langgraph.graph import StateGraph, END
from models.state import BlogState
from graph.nodes import topic_input_node, title_node, content_node
import os
from dotenv import load_dotenv

load_dotenv()

# LangSmith tracing
os.environ["LANGCHAIN_TRACING_V2"] = os.getenv("LANGCHAIN_TRACING_V2", "true")
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY", "")
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT", "blog-agent")

def build_graph():
    g = StateGraph(BlogState)

    g.add_node("topic_input", topic_input_node)
    g.add_node("title_agent", title_node)
    g.add_node("content_agent", content_node)

    g.set_entry_point("topic_input")
    g.add_edge("topic_input", "title_agent")
    g.add_edge("title_agent", "content_agent")
    g.add_edge("content_agent", END)

    return g.compile()

blog_graph = build_graph()