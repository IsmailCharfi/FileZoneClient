import kerberos
import requests
import json
from requests_kerberos import HTTPKerberosAuth
from typing import Callable


def kerberos_handshake(call: Callable[[dict], requests.Response]):
    try:
        headers = {}
        _, krb_context = kerberos.authGSSClientInit("host/client.filezone.com@FILEZONE.COM")
        kerberos.authGSSClientStep(krb_context, "")
        # grab the service ticket
        negotiate_details = kerberos.authGSSClientResponse(krb_context)
        # setup the auth header to use the kerberos ticket
        headers["Authorization"] = "Negotiate " + negotiate_details
        print("call")
        # make the request
        response = call(headers)

        # authenticate the service
        auth_header = response.headers["WWW-Authenticate"]
        service_auth = auth_header.split(" ")[1]
        kerberos.authGSSClientStep(krb_context, service_auth)
        kerberos.authGSSClientClean(krb_context)

        return response
    except Exception as e:
        print(str(e))
        return requests.Response()


class RestApi:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.auth = HTTPKerberosAuth()
        self.crt = "./certificate.crt"

    def get(self, path, params=None, use_kerberos=True):
        if use_kerberos:
            response = kerberos_handshake(
                lambda headers: self.session.get(self.base_url + path, headers=headers, params=params, verify=self.crt))
        else:
            response = requests.get(self.base_url + path, params=params, verify=self.crt)

        return response

    def post(self, path, data=None, files=None, use_kerberos=True):
        if data and isinstance(data, dict):
            data = json.dumps(data)

        if files:
            if use_kerberos:
                response = kerberos_handshake(lambda headers: self.session.post(self.base_url + path,
                                                                                     headers=headers, data=data,
                                                                                     files=files,
                                                                                     verify=self.crt))
            else:
                response = requests.post(self.base_url + path, data=data, files=files, verify=self.crt)
        else:
            if use_kerberos:
                response = kerberos_handshake(
                    lambda headers: self.session.post(self.base_url + path, headers=headers, json=data,
                                                      verify=self.crt))
            else:
                response = requests.post(self.base_url + path, json=data, verify=self.crt)

        return response

    def put(self, path, data=None, use_kerberos=True):
        if data and isinstance(data, dict):
            data = json.dumps(data)

        if use_kerberos:
            response = kerberos_handshake(
                lambda headers: self.session.put(self.base_url + path, headers=headers, data=data, verify=self.crt))
        else:
            response = requests.put(self.base_url + path, data=data, verify=self.crt)

        return response

    def delete(self, path, use_kerberos=True):
        if use_kerberos:
            response = kerberos_handshake(
                lambda headers: self.session.delete(self.base_url + path, headers=headers, verify=self.crt))
        else:
            response = requests.delete(self.base_url + path, verify=self.crt)

        return response
