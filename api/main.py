from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from graph.builder import blog_graph
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Blog Generation API")

class BlogRequest(BaseModel):
    topic: str
    blog_length: str = "long"

@app.get("/")
def home():
    return {"message": "Blog Generation API is running!"}

@app.post("/generate")
def generate_blog(request: BlogRequest):
    try:
        logger.info(f"Generating blog for topic: {request.topic}")
        
        result = blog_graph.invoke({
            "topic": request.topic,
            "context": "",
            "title_candidates": [],
            "chosen_title": "",
            "blog_length": request.blog_length,
            "blog_content": "",
            "final_output": ""
        })
        
        logger.info("Blog generated successfully!")
        
        return {
            "title": result["chosen_title"],
            "blog": result["final_output"]
        }
    
    except Exception as e:
        logger.error(f"Error generating blog: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Blog generation failed: {str(e)}"
        )