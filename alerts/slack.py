from wsgiref import headers
import requests
import json
from decouple import config

def send_alert(**kwargs):
    api_url = config('API_URL')
    headers = {"Content-type": "application/json"}
    message_body = kwargs.get('text', 'Vintage Bar Alert')
    message_body = {"text": message_body}
    response = requests.post(
                api_url,
                data = json.dumps(message_body),
                headers=headers            
            )
    
    
    
        
