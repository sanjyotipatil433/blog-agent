from typing import TypedDict, Optional, List

class BlogState(TypedDict):
    topic: str
    context: str
    title_candidates: List[str]
    chosen_title: str
    blog_length: str        # ← add this
    blog_content: str
    final_output: str