
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def LLMtest():
    stream = client.responses.create(
        model="gpt-4o-mini",
        input="Tell me a joke.",
        stream=True,
    )
 
    for event in stream:
        if hasattr(event, "type") and "text.delta" in event.type:
            yield event.delta

test = LLMtest()
for i in test:
    print(i, end="", flush=True)



