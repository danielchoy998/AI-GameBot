# Script Descriptions

This file provides a brief overview of some standalone or testing scripts within the project.

## `TTSmodel.py`

**Purpose:** This script provides functionality to convert text into Cantonese speech using the `cantonese.ai` API.

**Key Features:**
*   Loads the `CANTONESEAI_API_KEY` from the `.env` file.
*   Defines a `text_to_speech` function that takes text input and sends a request to the Cantonese.ai API with specified parameters (voice ID, speed, pitch, etc.).
*   Defines a `play_audio` function that takes the API response (audio data) and plays it using `pydub`.
*   Includes a `main` function (executed when the script is run directly) that allows interactive testing:
    *   Prompts the user to input text.
    *   Uses a default Cantonese phrase if no input is given.
    *   Calls the TTS function and plays the resulting audio.
    *   Allows the user to type `exit` to quit.

**Usage:** Can be run directly (`python TTSmodel.py`) for testing Cantonese text-to-speech conversion.

## `LocalLLM.py`

**Purpose:** This script functions as a text-only command-line chatbot interface that interacts with a locally running Ollama LLM.

**Key Features:**
*   Local LLM deployment with Ollama. (Model -> gemma3:4b)
*   Connects to a local Ollama instance using the `ollama` Python library.
*   Maintains a `conversation_history` list to provide context to the LLM.
*   Handles user input in a loop.
*   Streams the LLM's response back to the console chunk by chunk.
*   Includes basic error handling for Ollama API communication.
*   Allows the user to type `quit` or `exit` to end the chat.

**Usage:** Can be run directly (`python LocalLLM.py`) to chat with the specified Ollama model via the terminal, assuming Ollama is running and the model is available locally.

## `OpenAI.py`

**Purpose:** This script appears to be a simple, standalone test script specifically designed to interact with the OpenAI API's `responses.create` endpoint, likely for testing or demonstration purposes.

**Key Features:**
*   Loads the `OPENAI_API_KEY` from the `.env` file.
*   Initializes the OpenAI client.
*   Defines a function `LLMtest` that makes a hardcoded request to the `gpt-4o-mini` model with the input "Tell me a joke." using streaming.
*   Iterates through the streamed response events and yields the text deltas.
*   The main part of the script calls `LLMtest` and prints the yielded chunks to the console.

**Usage:** Can be run directly (`python OpenAI.py`) to perform a quick test of the OpenAI streaming API with a predefined prompt and model. Its functionality is largely superseded by `LLMmodel.py` for use within the main `app.py` application. 