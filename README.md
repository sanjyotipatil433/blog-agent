# AI Blog Generator 🚀
An autonomous blog generation engine built with LangGraph, FastAPI, and Streamlit.

## Architecture
- **LangGraph** — Multi-agent DAG workflow
- **FastAPI** — Backend microservice API
- **Streamlit** — Frontend UI
- **Groq (Llama3)** — Free LLM for content generation
- **LangSmith** — Real-time tracing and monitoring

## Agent Flow
Topic Input → Title Brainstorming Agent → Content Generation Agent → Final Blog

## Features
- Generate blogs from any topic
- Short (200-300 words) or Long (500-800 words)
- Dark/Light theme toggle
- Blog history with session memory
- Download blog as text file
- LangSmith observability

## Setup
1. Clone the repo

2. Create virtual environment:
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

3. Create `.env` file:
GROQ_API_KEY=your_groq_key
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_langsmith_key
LANGCHAIN_PROJECT=blog-agent

4. Run FastAPI:
```bash
uvicorn api.main:app --reload
```

5. Run Streamlit:
```bash
streamlit run app.py
```

## Project Structure
blog-agent/
├── agents/
│   ├── title_agent.py
│   └── content_agent.py
├── graph/
│   ├── nodes.py
│   ├── builder.py
├── models/
│   └── state.py
├── api/
│   └── main.py
├── app.py
├── requirements.txt
└── README.md

## Tech Stack
- Python 3.10+
- LangGraph
- LangChain
- FastAPI
- Streamlit
- Groq API