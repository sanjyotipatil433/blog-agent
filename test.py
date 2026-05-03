from graph.builder import blog_graph

# test input
result = blog_graph.invoke({
    "topic": "Benefits of Artificial Intelligence",
    "context": "",
    "title_candidates": [],
    "chosen_title": "",
    "blog_content": "",
    "final_output": ""
})

print("=== TITLES ===")
print(result["title_candidates"])

print("\n=== CHOSEN TITLE ===")
print(result["chosen_title"])

print("\n=== BLOG ===")
print(result["final_output"])