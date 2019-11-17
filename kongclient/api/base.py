# -*- coding: utf-8 -*-
from kongclient.exceptions import APIException


class Manager:

    def __init__(self, api):

        self.api = api

    def _list(self, url, response_key):

        resp = self.api.client.get(url=url)
        status_code = resp.status_code
        req_url = resp.request.url
        if status_code != 200:
            raise APIException(http_status=status_code, message=resp.text, method='GET', url=req_url)
        body = resp.json()
        return body[response_key]

    def _get(self, url):

        resp = self.api.client.get(url=url)
        status_code = resp.status_code
        req_url = resp.request.url
        if status_code != 200:
            raise APIException(http_status=status_code, message=resp.text, method='GET', url=req_url)
        body = resp.json()
        return body

    def _create(self, url, body):

        resp = self.api.client.post(url=url, json=body)
        status_code = resp.status_code
        req_url = resp.request.url
        if status_code != 201:
            raise APIException(http_status=status_code, message=resp.text, method='POST', url=req_url)
        body = resp.json()
        return body

    def _set(self, url):
        resp = self.api.client.post(url=url)
        status_code = resp.status_code
        req_url = resp.request.url
        if status_code != 204:
            raise APIException(http_status=status_code, message=resp.text, method='POST', url=req_url)
        return None

    def _update(self, url, body):

        resp = self.api.client.patch(url=url, json=body)
        status_code = resp.status_code
        req_url = resp.request.url
        if status_code != 200:
            raise APIException(http_status=status_code, message=resp.text, method='PATCH', url=req_url)
        body = resp.json()
        return body

    def _delete(self, url):

        resp = self.api.client.delete(url=url)
        status_code = resp.status_code
        req_url = resp.request.url
        if status_code != 204:
            raise APIException(http_status=status_code, message=resp.text, method='DELETE', url=req_url)
        return None
