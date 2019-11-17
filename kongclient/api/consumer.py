# -*- coding: utf-8 -*-
from kongclient.api import base


class ConsumerManager(base.Manager):
    """ Manager class for manipulating kong consumers. """

    FIELDS = ('username', 'custom_id', 'tags')

    def list(self, tags=None):
        if tags:
            return self._list(url='/consumers?tags=%s' % tags, response_key='data')
        return self._list(url='/consumers', response_key='data')

    def list_plugins(self, consumer_id):
        return self._list(url='/consumers/%s/plugins' % consumer_id, response_key='data')

    def get(self, consumer_id):
        return self._get(url='/consumers/%s' % consumer_id)

    def get_plugin(self, consumer_id, plugin_id):
        return self._get(url='/consumers/%s/plugins/%s' % (consumer_id, plugin_id))

    def create(self, username, custom_id=None, tags=None):
        body = {
            'username': username,
            'custom_id': custom_id,
            'tags': tags
        }
        return self._create(url='/consumers', body=body)

    def _update(self, url, **kwargs):
        body = {k: v for k, v in kwargs.items() if k in self.FIELDS}
        return super(ConsumerManager, self)._update(url=url, body=body)

    def update(self, consumer_id, **kwargs):
        return self._update(url='/consumers/%s' % consumer_id, **kwargs)

    def update_by_plugin(self, plugin_id, **kwargs):
        return self._update(url='/plugins/%s/consumer' % plugin_id, **kwargs)

    def delete(self, consumer_id):
        return self._delete(url='/consumers/%s' % consumer_id)

    def add_plugin(self, consumer_id, name, config=None, run_on='first',
                   protocols=('http', 'https'), enabled=True, tags=None):
        body = {
            'name': name,
            'run_on': run_on,
            'protocols': protocols,
            'enabled': enabled,
            'tags': tags or [name]
        }
        if config:
            body['config'] = config
        return self._create(url='/consumers/%s/plugins' % consumer_id, body=body)
