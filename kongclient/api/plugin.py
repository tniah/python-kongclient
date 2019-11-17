# -*- coding: utf-8 -*-
from kongclient.api import base


class PluginManager(base.Manager):
    """ Manager class for manipulating kong plugins. """

    FIELDS = ('name', 'route', 'service', 'consumer',
              'config', 'run_on', 'protocols', 'enabled', 'tags')

    def list(self, tags=None):
        if tags:
            return self._list(url='/plugins?tags=%s' % tags, response_key='data')
        return self._list(url='/plugins', response_key='data')

    def get(self, plugin_id):
        return self._get(url='/plugins/%s' % plugin_id)

    def get_enabled_plugins(self):
        return self._get(url='/plugins/enabled')

    def get_schema(self, plugin_id):
        return self._get(url='/plugins/schema/%s' % plugin_id)

    def get_service(self, plugin_id):
        return self._get(url='/plugins/%s/service' % plugin_id)

    def get_route(self, plugin_id):
        return self._get(url='/plugins/%s/route' % plugin_id)

    def get_consumer(self, plugin_id):
        return self._get(url='/plugins/%s/consumer' % plugin_id)

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

    def _update(self, url, **kwargs):
        body = {k: v for k, v in kwargs.items() if k in self.FIELDS}
        if 'route' in body and body['route']:
            body['route'] = {'id': body['route']}
        if 'service' in body and body['service']:
            body['service'] = {'id': body['service']}
        if 'consumer' in body and body['consumer']:
            body['consumer'] = {'id': body['consumer']}
        return super(PluginManager, self)._update(url=url, body=body)

    def update(self, plugin_id, **kwargs):
        return self._update(url='/plugins/%s' % plugin_id, **kwargs)

    def update_by_route(self, route_id, plugin_id, **kwargs):
        return self._update(url='/routes/%s/plugins/%s' % (route_id, plugin_id), **kwargs)

    def update_by_service(self, service_id, plugin_id, **kwargs):
        return self._update(url='/services/%s/plugins/%s' % (service_id, plugin_id), **kwargs)

    def update_by_consumer(self, consumer_id, plugin_id, **kwargs):
        return self._update(url='/consumers/%s/plugins/%s' % (consumer_id, plugin_id), **kwargs)

    def delete(self, plugin_id):
        return self._delete(url='/plugins/%s' % plugin_id)

    def delete_by_route(self, route_id, plugin_id):
        return self._delete(url='/routes/%s/plugins/%s' % (route_id, plugin_id))

    def delete_by_service(self, service_id, plugin_id):
        return self._delete(url='/services/%s/plugins/%s' % (service_id, plugin_id))

    def delete_by_consumer(self, consumer_id, plugin_id):
        return self._delete(url='/consumers/%s/plugins/%s' % (consumer_id, plugin_id))
