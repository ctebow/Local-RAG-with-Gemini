import os
import sys
from local_search import code_index
from ollama_agent import agent

# In-memory session history: { project_path: [query, response, ...] }
session_history = {}

def select_project(project_path):
    """Ensure the project exists and has an index."""
    if not os.path.exists(project_path):
        print(f"[ERROR] Project path does not exist: {project_path}")
        return None

    # Build index if missing
    index_dir = code_index.get_index_dir(project_path)
    if not os.path.exists(index_dir) or not os.listdir(index_dir):
        print(f"[INFO] Index not found for {project_path}, building now...")
        code_index.build_index(project_path)

    # Initialize history for this project
    if project_path not in session_history:
        session_history[project_path] = []

    return project_path

def query_project(project_path, query):
    """Query local code and LLM, store history, and print response."""
    # Query local code
    code_response = code_index.query_index(project_path, query)
    # Prompt LLM
    llm_response = agent.prompt_llm(query, code_context=str(code_response))
    
    # Store in session history
    session_history[project_path].append((query, llm_response))
    
    print("\n--- Response ---")
    print(llm_response)
    print("----------------\n")

def main():
    print("=== Local Coding Assistant ===")
    current_project = None

    while True:
        # Select project if none or user wants to switch
        if not current_project:
            project_path = input("Enter path to project (or 'exit' to quit): ").strip()
            if project_path.lower() == "exit":
                break
            current_project = select_project(project_path)
            if not current_project:
                continue

        # Get user query
        user_query = input(f"[{os.path.basename(current_project)}] Enter your question ('switch' to change project, 'exit' to quit): ").strip()
        if user_query.lower() == "exit":
            break
        elif user_query.lower() == "switch":
            current_project = None
            continue
        elif user_query == "":
            continue

        query_project(current_project, user_query)

if __name__ == "__main__":
    main()

