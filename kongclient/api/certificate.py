# -*- coding: utf-8 -*-
from kongclient.api import base


class CertificateManager(base.Manager):
    """ Manager class for manipulating kong cerfiticates. """

    FIELDS = ('cert', 'key', 'tags', 'snis')

    def list(self, tags):
        if tags:
            return self._list(url='/certificates?tags=%s' % tags, response_key='data')
        return self._list(url='/certificates', response_key='data')

    def get(self, certificate_id):
        return self._get(url='/certificates/%s' % certificate_id)

    def create(self, cert, key, snis=None, tags=None):
        body = {
            'cert': cert,
            'key': key,
            'snis': snis,
            'tags': tags
        }
        return self._create(url='/certificates', body=body)

    def update(self, certificate_id, **kwargs):
        body = {k: v for k, v in kwargs.items() if k in self.FIELDS}
        return self._update(url='/certificates/%s' % certificate_id, body=body)

    def delete(self, certificate_id):
        return self._delete(url='/certificates/%s' % certificate_id)
