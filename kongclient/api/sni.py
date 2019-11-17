# -*- coding: utf-8 -*-
from kongclient.api import base


class SNIManager(base.Manager):
    """ Manager class for manipulating kong SNIs. """

    FIELDS = ('name', 'certificate', 'tags')

    def list(self, tags=None):
        if tags:
            return self._list(url='/snis?tags=%s' % tags, response_key='data')
        return self._list(url='/snis', response_key='data')

    def get(self, sni_id):
        return self._get(url='/snis/%s' % sni_id)

    def create(self, name, certificate_id, tags=None):
        body = {
            'name': name,
            'certificate': {'id': certificate_id},
            'tags': tags or [name]
        }
        return self._create(url='/snis', body=body)

    def update(self, sni_id, **kwargs):
        body = {k: v for k, v in kwargs.items() if k in self.FIELDS}
        if 'certificate' in body and body['certificate']:
            body['certificate'] = {'id': body['certificate']}
        return self._update(url='/snis/%s' % sni_id, body=body)

    def delete(self, sni_id):
        return self._delete(url='/snis/%s' % sni_id)
