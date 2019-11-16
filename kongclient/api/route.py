# -*- coding: utf-8 -*-
from kongclient.api import base


class RouteManager(base.Manager):
    """ Manager class for manipulating kong routes. """

    FIELDS = ('name', 'hosts', 'protocols', 'methods', 'paths', 'headers',
              'https_redirect_status_code', 'regex_priority', 'strip_path',
              'preserve_host', 'snis', 'sources', 'destinations', 'service', 'tags')

    def list(self, tags=None):
        if tags:
            return self._list(url='/routes?tags=%s' % tags, response_key='data')
        return self._list(url='/routes', response_key='data')

    def get(self, route_id):
        return self._get(url='/routes/%s' % route_id)

    def create(self, name, hosts, service_id, protocols=('http', 'https'), headers=None,
               methods=('GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS', 'HEAD'), paths=None,
               https_redirect_status_code=426, regex_priority=0, strip_path=False, preserve_host=True,
               snis=None, sources=None, destinations=None, tags=None):
        body = {
            'name': name,
            'hosts': hosts,
            'protocols': protocols,
            'methods': methods,
            'paths': paths,
            'headers': headers,
            'https_redirect_status_code': https_redirect_status_code,
            'regex_priority': regex_priority,
            'strip_path': strip_path,
            'preserve_host': preserve_host,
            'snis': snis,
            'sources': sources,
            'destinations': destinations,
            'service': {'id': service_id},
            'tags': tags or [name]
        }
        return self._create(url='/routes', body=body)

    def update(self, route_id, **kwargs):
        body = {k: v for k, v in kwargs.items() if k in self.FIELDS}
        if 'service' in body and body['service']:
            body['service'] = {'id': body['service']}
        return self._update(url='/routes/%s' % route_id, body=body)

    def delete(self, route_id):
        return self._delete(url='/routes/%s' % route_id)

    def add_plugin(self, route_id, name, config=None, run_on='first',
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
        return self._create(url='/routes/%s/plugins' % route_id, body=body)
