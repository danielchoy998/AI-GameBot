document.addEventListener('DOMContentLoaded', () => {
    const chatContainer = document.getElementById('chat-container');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    // Optional: Get NPC selector if needed later
    // const npcSelect = document.getElementById('npc-select');

    // Function to add a message bubble to the chat
    function addMessageToChat(text, sender) {
        const messageDiv = document.createElement('div');
        const bubbleDiv = document.createElement('div');

        bubbleDiv.textContent = text;
        // Common bubble styles
        bubbleDiv.classList.add('text-gray-800', 'p-3', 'rounded-lg', 'max-w-xs', 'lg:max-w-md', 'shadow');

        if (sender === 'user') {
            messageDiv.classList.add('flex', 'justify-end', 'mb-3'); // Add margin bottom
            bubbleDiv.classList.add('bg-blue-100');
        } else { // AI
            messageDiv.classList.add('flex', 'justify-start', 'mb-3'); // Add margin bottom
            bubbleDiv.classList.add('bg-purple-100');
            bubbleDiv.id = 'ai-streaming-bubble'; // ID to potentially append to
        }

        messageDiv.appendChild(bubbleDiv);
        chatContainer.appendChild(messageDiv);

        // Scroll to the bottom
        chatContainer.scrollTop = chatContainer.scrollHeight;

        return bubbleDiv; // Return the bubble element
    }

    // Function to handle sending message and receiving stream
    async function sendMessage() {
        const messageText = userInput.value.trim();
        if (!messageText) return; // Don't send empty messages

        // Display user message
        addMessageToChat(messageText, 'user');
        userInput.value = ''; // Clear input field

        // --- Send message to backend and handle stream --- 
        let aiBubble = null; // Placeholder for the AI bubble we'll update
        let isFirstChunk = true;

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: messageText })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const reader = response.body.getReader();
            const decoder = new TextDecoder();

            while (true) {
                const { done, value } = await reader.read();
                if (done) {
                    console.log("Stream finished.");
                    if (aiBubble) aiBubble.removeAttribute('id'); // Clean up ID
                    break;
                }

                // Decode and process chunk
                const chunk = decoder.decode(value, { stream: true });
                
                // Server-Sent Events format: "data: {json_payload}\n\n"
                const lines = chunk.split('\n');
                for (const line of lines) {
                    if (line.startsWith('data:')) {
                        const jsonData = line.substring(5).trim();
                        if (jsonData) {
                            try {
                                const parsedData = JSON.parse(jsonData);
                                if (parsedData.error) {
                                    console.error('Backend Error:', parsedData.error);
                                    if(aiBubble) {
                                        aiBubble.textContent += `\n[Error: ${parsedData.error}]`;
                                    } else {
                                         addMessageToChat(`[Error: ${parsedData.error}]`, 'ai');
                                    }
                                    continue;
                                }
                                if (parsedData.text) {
                                    if (isFirstChunk) {
                                        aiBubble = addMessageToChat(parsedData.text, 'ai');
                                        isFirstChunk = false;
                                    } else if (aiBubble) {
                                        aiBubble.textContent += parsedData.text;
                                        chatContainer.scrollTop = chatContainer.scrollHeight; // Keep scrolling
                                    }
                                }
                            } catch (e) {
                                console.error('Error parsing JSON chunk:', jsonData, e);
                            }
                        }
                    } else if (line.trim() === '[DONE]') { // Handle potential [DONE] signal if sent outside data
                         console.log("Received [DONE] signal.");
                         if (aiBubble) aiBubble.removeAttribute('id'); 
                    }
                }
            }

        } catch (error) {
            console.error('Fetch error:', error);
            addMessageToChat(`Sorry, I encountered an error trying to respond. ${error.message || ''}`, 'ai');
             if (aiBubble) aiBubble.removeAttribute('id'); // Clean up ID on error too
        }
    }

    // Event Listeners
    sendButton.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (event) => {
        if (event.key === 'Enter') {
            sendMessage();
        }
    });

    // Add a welcome message
    addMessageToChat('Welcome to AI GameBot! How can I assist you?', 'ai');
}); 