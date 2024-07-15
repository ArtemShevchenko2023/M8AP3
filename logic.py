import json
import requests
from config import *
def generate(text):
    headers = {"Authorization": f"Bearer {api}"}
    ur = f"{url}"
    payload = {
    "providers": "openai, cohere",
    "text": f"{text}",
    "temperature" : 0.2,
    "max_tokens" : 250 }
    response = requests.post(ur, json=payload, headers=headers)
    result = json.loads(response.text)
    return result['openai']['generated_text']