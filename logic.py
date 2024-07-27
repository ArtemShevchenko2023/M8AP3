import json
import requests
from config import *
import time
import base64
from PIL import Image
from io import BytesIO
import sqlite3
def create_database():
    conn = sqlite3.connect('chatbot.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            request_text TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            request_id INTEGER,
            response_text TEXT,
            FOREIGN KEY (request_id) REFERENCES requests (id)
        )
    ''')
    conn.commit()
    conn.close()
def save_request_response(user_id, request_text, response_text):
    conn = sqlite3.connect('chatbot.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO requests (user_id, request_text) 
        VALUES (?, ?)
    ''', (user_id, request_text))
    request_id = cursor.lastrowid
    cursor.execute('''
        INSERT INTO responses (request_id, response_text) 
        VALUES (?, ?)
    ''', (request_id, response_text))
    conn.commit()
    conn.close()
create_database()
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
class Text2ImageAPI:
    def __init__(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }
    def get_model(self):
        response = requests.get(self.URL + 'key/api/v1/models', headers=self.AUTH_HEADERS)
        data = response.json()
        return data[0]['id']
    def generate(self, prompt, model, images=1, width=1024, height=1024):
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "generateParams": {
                "query": f"{prompt}"
            }
        }
        data = {
            'model_id': (None, model),
            'params': (None, json.dumps(params), 'application/json')
        }
        response = requests.post(self.URL + 'key/api/v1/text2image/run', headers=self.AUTH_HEADERS, files=data)
        data = response.json()
        return data['uuid']
    def check_generation(self, request_id, attempts=10, delay=10):
        while attempts > 0:
            response = requests.get(self.URL + 'key/api/v1/text2image/status/' + request_id, headers=self.AUTH_HEADERS)
            data = response.json()
            if data['status'] == 'DONE':
                return data['images']
            attempts -= 1
            time.sleep(delay)
    def conv(self, text):
        model = self.get_model()
        gen = self.generate(text, model)
        images = self.check_generation(gen)[0]
        base64_string = images
        decoded_data = base64.b64decode(base64_string)
        image = Image.open(BytesIO(decoded_data))
        image.save("decoded.jpg")
if __name__ == '__main__':
    api = Text2ImageAPI('https://api-key.fusionbrain.ai/', 'BB3D504A69D82D56C3A712CD169E1ADC', 'F001625BE2DD4C603995D8CEA8F16476')
    api.conv("Нейро-кот")
