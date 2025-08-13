from local_search.code_index import build_index
import os

PROJECTS_DIR = "projects"

def build_all_indices():
    for proj_name in os.listdir(PROJECTS_DIR):
        proj_path = os.path.join(PROJECTS_DIR, proj_name)
        if os.path.isdir(proj_path):
            print(f"Indexing project: {proj_name}")
            build_index(proj_path)

if __name__ == "__main__":
    build_all_indices()
