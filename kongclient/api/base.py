# -*- coding: utf-8 -*-
from kongclient.exceptions import APIException


class Manager:
    """ Basic manager type providing common operations.

     Managers interact with a particular type of API (routes, services, plugins, etc.)
     and provide CRUD operations for them.

     :param api: instance of KongClient for HTTP requests.
     """

    def __init__(self, api):
        self.api = api

    def _list(self, url, response_key):
        """ List the collection.

        :param url: a partial URL, e.g., '/services'
        :param response_key: the key to be looked up in response dictionary, e.g., 'data'
        """
        resp = self.api.client.get(url=url)
        if resp.status_code != 200:
            raise APIException(http_status=resp.status_code, message=resp.text, method='GET', url=resp.request.url)
        body = resp.json()
        return body[response_key]

    def _get(self, url):
        """ Get an object from collection.

        :param url: a partial URL, e.g., '/services/xxx_id'
        """
        resp = self.api.client.get(url=url)
        if resp.status_code != 200:
            raise APIException(http_status=resp.status_code, message=resp.text, method='GET', url=resp.request.url)
        body = resp.json()
        return body

    def _create(self, url, body):
        """ Create an object.

        :param url: a partial URL, e.g., '/services'
        :param body: data that will be encoded as JSON and passed in POST request
        """
        resp = self.api.client.post(url=url, json=body)
        if resp.status_code != 201:
            raise APIException(http_status=resp.status_code, message=resp.text, method='POST', url=resp.request.url)
        body = resp.json()
        return body

    def _set(self, url, body=None):
        """ Set value for object attribute.

        :param url: a partial URL, e.g., '/targets/xxx_id/healthy'
        """
        body = body if body is not None else {}
        resp = self.api.client.post(url=url, json=body)
        if resp.status_code != 204:
            raise APIException(http_status=resp.status_code, message=resp.text, method='POST', url=resp.request.url)
        return None

    def _update(self, url, body):
        """ Update an object with PATCH method.

        :param url: a partial URL, e.g., '/services/xxx_id'
        :param body: data that will be encoded as JSON and passed in PATCH request
        """
        resp = self.api.client.patch(url=url, json=body)
        if resp.status_code != 200:
            raise APIException(http_status=resp.status_code, message=resp.text, method='PATCH', url=resp.request.url)
        body = resp.json()
        return body

    def _delete(self, url):
        """ Delete an object.

        :param url: a partial URL, e.g., '/services/xxx_id'
        """
        resp = self.api.client.delete(url=url)
        if resp.status_code != 204:
            raise APIException(http_status= resp.status_code, message=resp.text, method='DELETE', url=resp.request.url)
        return None
