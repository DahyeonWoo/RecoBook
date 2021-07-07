import hashlib
import hmac
import base64
import time
import requests
import json


class ChatbotMessageSender:

    # chatbot api gateway url
    ep_path = 'https://20ede21bde4b4719b4d6ebb68880f80e.apigw.ntruss.com/custom/v1/4892/e7ce8f9fab706825ea5c03edcc053dbc8ebcb5b22ac1a8971c5bd83b201962ca'
    # chatbot custom secret key
    secret_key = 'S2V4elFrenVqbGNXQURQWnFKc2V2ZWJjZHJWdXdWc0c='

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
                        'description': 'About Me'
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
        #print(res.read().decode("UTF-8"))