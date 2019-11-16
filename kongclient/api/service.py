# -*- coding: utf-8 -*-
from kongclient.api import base


class ServiceManager(base.Manager):
    """ Manager class for manipulating kong services. """

    FIELDS = ('name', 'protocol', 'host', 'port', 'path', 'url', 'retries',
              'connect_timeout', 'write_timeout', 'read_timeout', 'client_certificate', 'tags')

    def list(self):
        return self._list(url='/services', response_key='data')

    def get(self, service_id):
        return self._get(url='/services/%s' % service_id)

    def create(self, name, url=None, protocol='http', host=None, port=80, path=None,
               retries=5, connect_timeout=60000, write_timeout=60000, read_timeout=60000,
               client_certificate=None, tags=None):
        body = {
            'name': name,
            'retries': retries,
            'connect_timeout': connect_timeout,
            'write_timeout': write_timeout,
            'read_timeout': read_timeout,
            'tags': tags or [name]
        }
        if not url:
            body.update({'protocol': protocol, 'host': host, 'port': port, 'path': path})
        else:
            body['url'] = url
        if client_certificate:
            body['client_certificate'] = {'id': client_certificate}
        return self._create(url='/services', body=body)

    def update(self, service_id, **kwargs):
        body = {k: v for k, v in kwargs.items() if k in self.FIELDS}
        if 'client_certificate' in body and body['client_certificate']:
            body['client_certificate'] = {'id': body['client_certificate']}
        return self._update(url='/services/%s' % service_id, body=body)

    def delete(self, service_id):
        return self._delete(url='/services/%s' % service_id)
