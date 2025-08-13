import subprocess

DEFAULT_MODEL = "codellama:7b"
DEFAULT_TEMP = 0.2

def prompt_llm(user_prompt, code_context="", model=DEFAULT_MODEL, temp=DEFAULT_TEMP):
    """
    Sends a prompt to the local Ollama server with optional code context and returns the response.
    
    Parameters:
    - user_prompt: str, the user's natural language query.
    - code_context: str, optional code snippets or local project info to provide context.
    - model: str, Ollama model to use.
    - temp: float, temperature for response randomness.
    
    Returns:
    - str: The model's response text.
    """
    # Combine the user's prompt with code context
    full_prompt = user_prompt
    if code_context:
        full_prompt = f"Context:\n{code_context}\n\nQuestion:\n{user_prompt}"

    try:
        cmd = [
            "ollama", "run", model, full_prompt, "Only respond with code, and nothing else."
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        response = result.stdout.strip()
    except subprocess.CalledProcessError as e:
        response = f"[ERROR] Ollama call failed: {e}"
    except Exception as e:
        response = f"[ERROR] Unexpected error: {e}"

    return response

