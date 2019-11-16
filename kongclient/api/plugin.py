# -*- coding: utf-8 -*-
from kongclient.api import base


class PluginManager(base.Manager):
    """ Manager class for manipulating kong plugins. """

    FIELDS = ('name', 'route', 'service', 'consumer',
              'config', 'run_on', 'protocols', 'enabled', 'tags')

    def list(self):
        return self._list(url='/plugins', response_key='data')

    def get(self, plugin_id):
        return self._get(url='/plugins/%s' % plugin_id)

    def create(self, name, route_id=None, service_id=None, consumer_id=None, config=None,
               run_on='first', protocols=('http', 'https'), enabled=True, tags=None):
        body = {
            'name': name,
            'run_on': run_on,
            'protocols': protocols,
            'enabled': enabled,
            'tags': tags or [name]
        }
        if route_id:
            body['route'] = {'id': route_id}
        if service_id:
            body['service'] = {'id': service_id}
        if consumer_id:
            body['consumer'] = {'id': consumer_id}
        if config:
            body['config'] = config
        return self._create(url='/plugins', body=body)

    def update(self, plugin_id, **kwargs):
        body = {k: v for k, v in kwargs.items() if k in self.FIELDS}
        if 'route' in body and body['route']:
            body['route'] = {'id': body['route']}
        if 'service' in body and body['service']:
            body['service'] = {'id': body['service']}
        if 'consumer' in body and body['consumer']:
            body['consumer'] = {'id': body['consumer']}
        return self._update(url='/plugins/%s' % plugin_id, body=body)
