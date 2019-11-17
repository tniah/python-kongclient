# -*- coding: utf-8 -*-
from kongclient.api import base


class CertificateManager(base.Manager):
    """ Manager class for manipulating kong cerfiticates. """

    FIELDS = ('cert', 'key', 'tags', 'snis')

    def list(self, tags):
        if tags:
            return self._list(url='/certificates?tags=%s' % tags, response_key='data')
        return self._list(url='/certificates', response_key='data')

    def list_services(self, certificate_id):
        return self._list(url='/certificates/%s/services' % certificate_id, response_key='data')

    def list_snis(self, certificate_id):
        return self._list(url='/certificates/%s/snis' % certificate_id, response_key='data')

    def get(self, certificate_id):
        return self._get(url='/certificates/%s' % certificate_id)

    def get_service(self, certificate_id, service_id):
        return self._get(url='/certificates/%s/services/%s' % (certificate_id, service_id))

    def get_sni(self, certificate_id, sni_id):
        return self._get(url='/certificates/%s/snis/%s' % (certificate_id, sni_id))

    def create(self, cert, key, snis=None, tags=None):
        body = {'cert': cert, 'key': key, 'snis': snis, 'tags': tags}
        return self._create(url='/certificates', body=body)

    def update(self, certificate_id, **kwargs):
        body = {k: v for k, v in kwargs.items() if k in self.FIELDS}
        return self._update(url='/certificates/%s' % certificate_id, body=body)

    def delete(self, certificate_id):
        return self._delete(url='/certificates/%s' % certificate_id)

    def add_service(self, certificate_id, name, url=None, protocol='http', host=None, port=80, path=None,
                    retries=5, connect_timeout=60000, write_timeout=60000, read_timeout=60000, tags=None):
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
        return self._create(url='/certificates/%s/services' % certificate_id, body=body)

    def add_sni(self, certificate_id, name, tags=None):
        body = {'name': name, 'tags': tags or [name]}
        return self._create(url='/certificates/%s/snis' % certificate_id, body=body)
