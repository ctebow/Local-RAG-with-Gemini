# Gemini Context: Local RAG Pipeline

## Project Overview

This project is a command-line-based Retrieval-Augmented Generation (RAG) pipeline. Its primary function is to allow a user to select a local code repository, automatically vectorize it to create a searchable index, and then use that index to inject relevant code context into a Large Language Model (LLM) prompt based on a user's query.

The goal is to provide a powerful, context-aware coding assistant by leveraging local codebases for accurate and relevant prompt augmentation.

## Workflow

The user interacts with the system through a command-line interface (`main.py`). The process is as follows:

1.  **Project Selection**: The user provides a file path to a local project directory.
2.  **Indexing**: The system checks if a vector index for this project already exists. If not, it automatically builds one using the `local_search/code_index.py` module. The index is stored in the `index_storage/` directory.
3.  **User Query**: The user asks a question about the selected project.
4.  **Context Retrieval**: The system queries the project's vector index to find code snippets that are most relevant to the user's question.
5.  **Prompt Augmentation**: The retrieved code snippets are formatted and combined with the original user query to form a detailed prompt.
6.  **LLM Interaction**: The augmented prompt is sent to an LLM (currently a local Ollama model via `ollama_agent/agent.py`).
7.  **Response**: The LLM's response is displayed to the user.

The application maintains a simple in-memory session history of queries and responses for each project.

## Core Components

-   **`main.py`**: The main entry point and command-line interface for the application. It handles user interaction, project selection, and orchestrates the overall workflow.
-   **`local_search/code_index.py`**: This module is responsible for creating, storing, and querying the vector indexes of the code projects. It handles the vectorization of the codebase.
-   **`ollama_agent/agent.py`**: This module acts as the interface to the LLM. It takes the augmented prompt and communicates with the language model to get a response.
-   **`index_storage/`**: This directory serves as the persistent storage for the generated vector indexes. Each project gets its own subdirectory for its index.
-   **`dev_venv/`**: The Python virtual environment for managing project dependencies.

## How to Run

The application is run from the command line:

```bash
python main.py
```

1.  The script will first ask for the path to the project you want to work with.
2.  If no index exists for that project, it will be created automatically.
3.  Once the project is selected, you can enter your questions at the prompt.
4.  To switch to a different project, type `switch`.
5.  To quit the application, type `exit`.

## Integration Goal

The primary objective is to replace the current local `ollama_agent` with an integration to Google's Gemini API. The goal is to leverage Gemini's large context window and powerful reasoning capabilities to provide more comprehensive and accurate answers by feeding it the context retrieved from the local code search.
