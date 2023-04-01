import requests
import json


class RestApi:
    def __init__(self, base_url):
        self.base_url = base_url

    def get(self, path, headers=None, params=None, files=None, decrypt=False):
        response = requests.get(self.base_url + path, headers=headers, params=params, files=files)
        if response.headers.get('content-type') == 'application/json':
            if decrypt:
                content = self.decrypt(response.content)
            else:
                content = response.content
            return json.loads(content)
        else:
            return response.content

    def post(self, path, data=None, headers=None, files=None, encrypt=False):
        if data and isinstance(data, dict):
            data = json.dumps(data)
        if files:
            response = requests.post(self.base_url + path, headers=headers, data=data, files=files)
        else:
            response = requests.post(self.base_url + path, headers=headers, json=data)
        if encrypt:
            return self.encrypt(response.content)
        else:
            return response

    def put(self, path, data=None, headers=None, files=None, encrypt=False):
        if data and isinstance(data, dict):
            data = json.dumps(data)
        if files:
            response = requests.put(self.base_url + path, headers=headers, data=data, files=files)
        else:
            response = requests.put(self.base_url + path, headers=headers, data=data)
        if encrypt:
            return self.encrypt(response.content)
        else:
            return response.content

    def delete(self, path, headers=None):
        response = requests.delete(self.base_url + path, headers=headers)
        return response.content

    def encrypt(self, data):
        # add encryption logic here
        return data

    def decrypt(self, data):
        # add decryption logic here
        return data
