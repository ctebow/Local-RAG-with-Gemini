# In gemini_agent/agent.py

def format_prompt_for_cli(user_prompt, code_context=""):
    """
    Formats the user's query and retrieved code context into a single string
    that can be easily copied and pasted into the Gemini CLI.
    """
    # --- Prompt Formatting for CLI ---
    # The prompt is structured to give Gemini clear instructions and context.
    # 1. **System Instruction**: A clear role and goal for the AI.
    # 2. **Code Context**: The retrieved code snippets, clearly demarcated.
    # 3. **User's Question**: The specific user query.

    system_instruction = "You are an expert software engineer and coding assistant."

    if code_context:
        # Format the context to be clearly readable
        full_prompt = f"{system_instruction}\n\n"
        full_prompt += f"--- Start of Retrieved Code Context ---\n"
        full_prompt += f"{code_context}\n"
        full_prompt += f"--- End of Retrieved Code Context ---\n\n"
        full_prompt += f"Based on the code context above, please answer the following question:\n"
        full_prompt += f"Question: {user_prompt}\n"
    else:
        # Prompt without code context
        full_prompt = f"{system_instruction}\n\n"
        full_prompt += f"Please answer the following question:\n"
        full_prompt += f"Question: {user_prompt}\n"

    return full_prompt