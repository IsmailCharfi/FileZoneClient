import requests
import json
from requests_kerberos import HTTPKerberosAuth


class RestApi:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.auth = HTTPKerberosAuth()
        self.crt = "./certificate.crt"

    def get(self, path, headers=None, params=None, kerberos=True):
        if kerberos:
            response = self.session.get(self.base_url + path, headers=headers, params=params, verify=self.crt)
        else:
            response = requests.get(self.base_url + path, headers=headers, params=params, verify=self.crt)

        return response

    def post(self, path, data=None, headers=None, files=None, kerberos=True):
        if data and isinstance(data, dict):
            data = json.dumps(data)

        if files:
            if kerberos:
                response = self.session.post(self.base_url + path, headers=headers, data=data, files=files,
                                             verify=self.crt)
            else:
                response = requests.post(self.base_url + path, headers=headers, data=data, files=files, verify=self.crt)
        else:
            if kerberos:
                response = self.session.post(self.base_url + path, headers=headers, json=data, verify=self.crt)
            else:
                response = requests.post(self.base_url + path, headers=headers, json=data, verify=self.crt)

        return response

    def put(self, path, data=None, headers=None, files=None, kerberos=True):
        if data and isinstance(data, dict):
            data = json.dumps(data)
        if files:
            if kerberos:
                response = self.session.put(self.base_url + path, headers=headers, data=data, files=files,
                                            verify=self.crt)
            else:
                response = requests.put(self.base_url + path, headers=headers, data=data, files=files, verify=self.crt)

        else:
            if kerberos:
                response = self.session.put(self.base_url + path, headers=headers, data=data, verify=self.crt)
            else:
                response = requests.put(self.base_url + path, headers=headers, data=data, verify=self.crt)

        return response

    def delete(self, path, headers=None, kerberos=True):
        if kerberos:
            response = self.session.delete(self.base_url + path, headers=headers, verify=self.crt)
        else:
            response = requests.delete(self.base_url + path, headers=headers, verify=self.crt)

        return response

