# -*- coding: utf-8 -*-
from kongclient.api import base


class UpstreamManager(base.Manager):
    """ Manager class for manipulating kong upstreams. """

    FIELDS = ('name', 'algorithm', 'hash_on', 'hash_fallback', 'hash_on_header', 'hash_fallback_header',
              'hash_on_cookie', 'hash_on_cookie_path', 'slots', 'healthchecks', 'tags', 'host_header')

    def list(self, tags=None):
        if tags:
            return self._list(url='/upstreams?tags=%s' % tags, response_key='data')
        return self._list(url='/upstreams', response_key='data')

    def list_targets(self, upstream_id):
        return self._list(url='/upstreams/%s/targets' % upstream_id, response_key='data')

    def list_all_targets(self, upstream_id):
        return self._list(url='/upstreams/%s/targets/all/' % upstream_id, response_key='data')

    def get(self, upstream_id):
        return self._get('/upstreams/%s' % upstream_id)

    def get_upstream_health(self, upstream_id):
        return self._get(url='/upstreams/%s/health/' % upstream_id)

    def create(self, name, algorithm='round-robin', hash_on='none', hash_fallback='none', hash_on_header=None,
               hash_fallback_header=None, hash_on_cookie=None, hash_on_cookie_path='/', slots=10000,
               healthchecks=None, tags=None, host_header=None):
        body = {
            'name': name,
            'algorithm': algorithm,
            'hash_on': hash_on,
            'hash_fallback': hash_fallback,
            'hash_on_header': hash_on_header,
            'hash_fallback_header': hash_fallback_header,
            'hash_on_cookie': hash_on_cookie,
            'hash_on_cookie_path': hash_on_cookie_path,
            'slots': slots,
            'healthchecks': healthchecks,
            'host_header': host_header,
            'tags': tags or [name]
        }
        return self._create(url='/upstreams', body=body)

    def _update(self, url, **kwargs):
        body = {k: v for k, v in kwargs.items() if k in self.FIELDS}
        return super(UpstreamManager, self)._update(url=url, body=body)

    def update(self, upstream_id, **kwargs):
        return self._update(url='/upstreams/%s' % upstream_id, **kwargs)

    def update_by_target(self, target_id, **kwargs):
        return self._update(url='/targets/%s/upstream' % target_id, **kwargs)

    def delete(self,  upstream_id):
        return self._delete(url='/upstreams/%s' % upstream_id)

    def delete_by_target(self, target_id):
        return self._delete(url='/targets/%s/upstream' % target_id)

    def add_target(self, upstream_id, target, weight=100, tags=None):
        body = {'target': target, 'weight': weight, 'tags': tags or [target]}
        return self._create(url='/upstreams/%s/targets' % upstream_id, body=body)

