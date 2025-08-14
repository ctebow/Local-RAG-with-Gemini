# Local RAG Pipeline for Gemini CLI

This project implements a local Retrieval-Augmented Generation (RAG) pipeline designed to work with the Gemini CLI. It allows you to use your own codebases as a source of context, which can then be seamlessly injected into your prompts when interacting with Gemini.

## How it Works

The workflow is designed to be simple and efficient:

1.  **Run the Script**: Execute the main CLI script.
2.  **Select a Project**: Provide the file path to a local code repository you want to work with.
3.  **Automatic Indexing**: If an index for the project doesn't exist, the script will automatically create a vector index of the codebase. This index is stored in the `index_storage/` directory for future use.
4.  **Ask a Question**: Enter your query or question about the codebase.
5.  **Generate a Prompt**: The script searches the vector index to find the most relevant code snippets related to your query.
6.  **Copy to Gemini**: The script then formats these snippets and your question into a complete prompt that is printed to the console. You can simply copy this entire output and paste it into your Gemini CLI chat.

## How to Use

1.  Ensure you have the necessary Python packages installed from the `dev_venv` virtual environment.
2.  Run the main CLI script from your terminal:
    ```bash
    python main_cli.py
    ```
3.  Follow the on-screen prompts to select a project and ask your questions.

## Core Components

-   **`main_cli.py`**: The main entry point and command-line interface for the application.
-   **`local_search/`**: Contains the logic for creating, storing, and querying the vector indexes of your code projects.
-   **`gemini_agent/`**: Contains the logic for formatting the final prompt to be used with the Gemini CLI.
-   **`index_storage/`**: The default storage directory for the generated vector indexes.