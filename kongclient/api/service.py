# -*- coding: utf-8 -*-
from kongclient.api import base


class ServiceManager(base.Manager):
    """ Manager class for manipulating kong services. """

    FIELDS = ('name', 'protocol', 'host', 'port', 'path', 'url', 'retries',
              'connect_timeout', 'write_timeout', 'read_timeout', 'client_certificate', 'tags')

    def list(self, tags=None):
        if tags:
            return self._list(url='/services?tags=%s' % tags, response_key='data')
        return self._list(url='/services', response_key='data')

    def list_routes(self, service_id):
        return self._list(url='/services/%s/routes' % service_id, response_key='data')

    def list_plugins(self, service_id):
        return self._list(url='/services/%s/plugins' % service_id, response_key='data')

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

    def add_route(self, service_id, name, hosts, protocols=('http', 'https'), headers=None,
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
            'tags': tags or [name]
        }
        return self._create(url='/services/%s/routes' % service_id, body=body)

    def add_plugin(self, service_id, name, config=None, run_on='first',
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
        return self._create(url='/services/%s/plugins' % service_id, body=body)
