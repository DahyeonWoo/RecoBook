import hashlib
import hmac
import base64
import requests
import json
from datetime import datetime
import time
from decouple import config


class ChatbotMessageSender:
    # chatbot api gateway url
    ep_path = config("INVOKE_URL")
    # chatbot custom secret key
    secret_key = config("SECRET_KEY")

    def req_message_send(self):

        timestamp = self.get_timestamp()
        request_body = {
            'version': 'v2',
            'userId': 'U47b00b58c90f8e47428af8b7bddcda3d1111111',
            'timestamp': timestamp,
            'bubbles': [
                {
                    'type': 'text',
                    'data': {
                        'description': '로맨스 장르 책 추천해줘'
                    }
                }
            ],
            'event': 'send'
        }

        ## Request body
        encode_request_body = json.dumps(request_body).encode('UTF-8')

        ## make signature
        signature = self.make_signature(self.secret_key, encode_request_body)

        ## headers
        custom_headers = {
            'Content-Type': 'application/json;UTF-8',
            'X-NCP-CHATBOT_SIGNATURE': signature
        }

        print("## Timestamp : ", timestamp)
        print("## Signature : ", signature)
        print("## headers ", custom_headers)
        print("## Request Body : ", encode_request_body)

        ## POST Request
        response = requests.post(headers=custom_headers, url=self.ep_path, data=encode_request_body)

        return response
        
    def success(self):
        timestamp = self.get_timestamp()
        request_body = {
            "version": "v2",
            "userId": "U47b00b58c90f8e47428af8b7bddcda3d",
            "sessionId": "34a59946-5dcb-4b72-9b63-a773c659702e",
            "timestamp": timestamp,
            # "bubbles": [ // each component is a bubble ],
            # "quickButtons": [ // some buttons ],
            "scenario": {
            "name": "analyzedScenarioName",
            # "intent": [ // some scenario intent ] 
                        },
            "entities": [ {
            "word": "userInputWord",
            "name": "analyzedEntityName" } ],
            "keywords": [ {
            "keyword": "userInputKeyword",
            "group": "analyzedKeywordGroupName",
            "type": "analyzedKeywordType" } ],
            # "persistentMenu": { // one template component },
            "event": "send"
        }

        ## Request body
        encode_request_body = json.dumps(request_body).encode('UTF-8')

        ## make signature
        signature = self.make_signature(self.secret_key, encode_request_body)

        ## headers
        custom_headers = {
            'Content-Type': 'application/json;UTF-8',
            'X-NCP-CHATBOT_SIGNATURE': signature
        }

        print("## Timestamp : ", timestamp)
        print("## Signature : ", signature)
        print("## headers ", custom_headers)
        print("## Request Body : ", encode_request_body)

        ## POST Request
        response = requests.post(headers=custom_headers, url=self.ep_path, data=encode_request_body)

        return response

    @staticmethod
    def get_timestamp():
        timestamp = int(time.time() * 1000)
        return timestamp

    @staticmethod
    def make_signature(secret_key, request_body):

        secret_key_bytes = bytes(secret_key, 'UTF-8')

        signing_key = base64.b64encode(hmac.new(secret_key_bytes, request_body, digestmod=hashlib.sha256).digest())

        return signing_key


if __name__ == '__main__':
    
    res = ChatbotMessageSender().req_message_send()

    print(res.status_code)
    if(res.status_code == 200):
        print(res.text)
        # print(res.read().decode("UTF-8"))