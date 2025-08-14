import os
import sys
from local_search import code_index
from gemini_agent import agent

# This version is modified to output a prompt for the Gemini CLI
# instead of calling an API.

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

    return project_path

def generate_cli_prompt(project_path, query):
    """
    Queries local code, formats a prompt for the Gemini CLI,
    and prints it to the console.
    """
    # Query local code
    code_response = code_index.query_index(project_path, query)
    
    # Format the prompt for the CLI
    cli_prompt = agent.format_prompt_for_cli(query, code_context=str(code_response))
    
    print("\n" + "="*60)
    print("COPY AND PASTE THE FOLLOWING PROMPT INTO THE GEMINI CLI:")
    print("="*60 + "\n")
    print(cli_prompt)
    print("\n" + "="*60)
    print("END OF PROMPT")
    print("="*60 + "\n")


def main():
    print("=== Local Coding Assistant (CLI Prompt Generator) ===")
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

        generate_cli_prompt(current_project, user_query)

if __name__ == "__main__":
    main()
