import subprocess
import re

DEFAULT_MODEL = "deepseek-coder:1.3b"
DEFAULT_TEMP = 0.2

def prompt_llm(user_prompt, code_context="", model=DEFAULT_MODEL, temp=DEFAULT_TEMP):
    """
    Sends a prompt to the local Ollama server with optional code context and returns only code.
    """
    # Build prompt with strong instruction
    instruction = "You are a code generator. ONLY RETURN CODE. Do NOT include explanations or comments."
    full_prompt = f"{instruction}\n\n"
    if code_context:
        full_prompt += f"Context:\n{code_context}\n\n"
    full_prompt += f"Question:\n{user_prompt}"
    
    try:
        cmd = [
            "ollama", "run", model, full_prompt,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        response = result.stdout.strip()
        
        # Post-process: extract code blocks if present
        code_matches = re.findall(r"```(?:\w+)?\n(.*?)```", response, flags=re.DOTALL)
        if code_matches:
            response = "\n".join(code_matches)

    except subprocess.CalledProcessError as e:
        response = f"[ERROR] Ollama call failed: {e}"
    except Exception as e:
        response = f"[ERROR] Unexpected error: {e}"

    return response


