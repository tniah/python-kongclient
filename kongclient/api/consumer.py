# -*- coding: utf-8 -*-
from kongclient.api import base


class ConsumerManager(base.Manager):
    """ Manager class for manipulating kong consumers. """

    FIELDS = ('username', 'custom_id', 'tags')

    def list(self, tags=None):
        if tags:
            return self._list(url='/consumers?tags=%s' % tags, response_key='data')
        return self._list(url='/consumers', response_key='data')

    def get(self, consumer_id):
        return self._get(url='/consumers/%s' % consumer_id)

    def create(self, username, custom_id=None, tags=None):
        body = {
            'username': username,
            'custom_id': custom_id,
            'tags': tags
        }
        return self._create(url='/consumers', body=body)

    def update(self, consumer_id, **kwargs):
        body = {k: v for k, v in kwargs.items() if k in self.FIELDS}
        return self._update(url='/consumers/%s' % consumer_id, body=body)

    def delete(self, consumer_id):
        return self._delete(url='/consumers/%s' % consumer_id)
