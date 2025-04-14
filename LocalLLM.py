import sys
# Removed os and httpx imports as they were only for image loading
from ollama import chat, ResponseError

# --- Ollama Interaction ---

def get_ollama_response(model_name: str, conversation_history: list[dict]) -> str | None:
    """Sends the conversation history to Ollama and streams the response.

    Args:
        model_name: The name of the Ollama model to use.
        conversation_history: The list of message dictionaries representing the conversation.

    Returns:
        The full assistant response as a string, or None if an error occurred.
    """
    try:
        print(f"Assistant: ", end='', flush=True) # Print prefix before streaming starts
        response_stream = chat(
            model=model_name,
            messages=conversation_history, # Send the whole history (now text-only)
            stream=True
        )

        full_response_content = []
        for chunk in response_stream:
            if chunk and 'message' in chunk and 'content' in chunk['message']:
                content = chunk['message']['content']
                print(content, end='', flush=True) # Stream content without prefix
                full_response_content.append(content)
            elif chunk and 'done' in chunk and chunk['done']:
                 if 'total_duration' in chunk:
                     pass # Optional: Handle duration
                 else:
                    print() # Ensure newline after streaming is done
                 break # Exit loop once done
            elif chunk and 'error' in chunk:
                 print(f"\nError during streaming: {chunk['error']}", file=sys.stderr)
                 return None # Stop processing on stream error

        return "".join(full_response_content)

    except ResponseError as e:
        print(f"\nOllama API error: {e.error} (Status: {getattr(e, 'status_code', 'N/A')})", file=sys.stderr)
    except Exception as e:
        print(f"\nAn error occurred during Ollama chat: {e}", file=sys.stderr)
    return None

# --- Main Execution --- #

if __name__ == '__main__':
    print("--- Local Ollama Chatbot (Text-Only) ---")
    # Hardcoded model name
    model_name = "gemma3:4b"
    print(f"Using model: {model_name}")
    print("Type your message.")
    print("Type 'quit' or 'exit' to end the chat.")
    print("-------------------------------------")

    conversation_history = []
    
    while True:
        user_input = input("You: ")

        if user_input.lower() in ["quit", "exit"]:
            print("Exiting chatbot.")
            break

        user_message = {
            "role": "user",
            "content": user_input
        }
    
        conversation_history.append(user_message)
        assistant_response = get_ollama_response(model_name, conversation_history)

        if assistant_response is not None: 
            conversation_history.append({
                "role": "assistant",
                "content": assistant_response
            })
        else:
            # If Ollama failed, remove the user message that caused the error
            conversation_history.pop()
            print("-> Assistant failed to respond. Please try again.")