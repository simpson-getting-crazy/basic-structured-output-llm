from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel
import os
import sys
import json

load_dotenv()

class CalendarEvent(BaseModel):
    name: str
    date: str
    participants: list[str]

# Check for required environment variables
api_key = os.getenv('OPENAI_API_KEY')
base_url = os.getenv('OPENAI_BASE_URL')

if not api_key or not base_url:
    print("Error: Missing required environment variables.")
    print("Please ensure OPENAI_API_KEY and OPENAI_BASE_URL are set in your .env file.")
    sys.exit(1)

client = OpenAI(
    base_url=base_url,
    api_key=api_key,
    default_headers={
        "HTTP-Referer": "https://github.com/OpenRouterAPI/example",
    }
)

completion = client.chat.completions.create(
    model="openai/gpt-4o-2024-11-20",
    messages=[
        {
            "role": "system",
            "content": "Extract the event information and respond with a JSON object containing 'name' (string), 'date' (string), and 'participants' (array of strings)."
        },
        {
            "role": "user",
            "content": "Alice and Bob are going to a science fair on Friday."
        }
    ],
    response_format={ "type": "json_object" }
)

response_text = completion.choices[0].message.content
event_dict = json.loads(response_text)
event = CalendarEvent(**event_dict)

print({
    "Event Name": event.name,
    "Event Date": event.date,
    "Event Participants": event.participants
})