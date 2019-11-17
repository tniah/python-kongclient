# -*- coding: utf-8 -*-
from kongclient.api import base


class UpstreamManager(base.Manager):
    """ Manager class for manipulating kong upstreams. """

    FIELDS = ('name', 'algorithm', 'hash_on', 'hash_fallback', 'hash_on_header', 'hash_fallback_header',
              'hash_on_cookie', 'hash_on_cookie_path', 'slots', 'healthchecks', 'tags', 'host_header')

    def list(self, tags=None):
        """ Get a list of upstreams.

        :param tags: A string associated to Upstreams in Kong, e.g, 'admin,example'
        """
        if tags:
            return self._list(url='/upstreams?tags=%s' % tags, response_key='data')
        return self._list(url='/upstreams', response_key='data')

    def list_targets(self, upstream_id):
        """ Get a list of targets associated to a specific upstream.

        :param upstream_id: The unique identifier or the name attribute
        of the Upstream whose Targets are to be retrieved.
        """
        return self._list(url='/upstreams/%s/targets' % upstream_id, response_key='data')

    def list_all_targets(self, upstream_id):
        """ Get a list of all targets associated to a specific upstream.

        :param upstream_id: The unique identifier or the name attribute
        of the Upstream whose Targets are to be retrieved.
        """
        return self._list(url='/upstreams/%s/targets/all/' % upstream_id, response_key='data')

    def get(self, upstream_id):
        """ Get details of a Upstream.

        :param upstream_id: The unique identifier or the name of the Upstream to retrieve.
        """
        return self._get('/upstreams/%s' % upstream_id)

    def get_upstream_health(self, upstream_id):
        """ Show upstream health for node.

        :param upstream_id: The unique identifier or the name of the Upstream to retrieve.
        """
        return self._get(url='/upstreams/%s/health/' % upstream_id)

    def create(self, name, algorithm='round-robin', hash_on='none', hash_fallback='none', hash_on_header=None,
               hash_fallback_header=None, hash_on_cookie=None, hash_on_cookie_path='/', slots=10000,
               healthchecks=None, tags=None, host_header=None):
        """ Create a upstream.

        :param name: This is a hostname, which must be equal to the host of a Service.
        :param algorithm: Which load balancing algorithm to use.
        One of: `round-robin`, `consistent-hashing`, or `least-connections`.
        :param hash_on: What to use as hashing input: `none`
        (resulting in a weighted-round-robin scheme with no hashing),
        `consumer`, `ip`, `header`, or `cookie`.
        :param hash_fallback: What to use as hashing input if the primary `hash_on`
        does not return a hash (eg. header is missing, or no consumer identified).
        One of: `none`, `consumer`, `ip`, `header`, or `cookie`.Not available if `hash_on` is set to `cookie`.
        :param hash_on_header: The header name to take the value from as hash input.
        Only required when `hash_on` is set to `header`.
        :param hash_fallback_header: The header name to take the value from as hash input.
        Only required when `hash_fallback` is set to `header`.
        :param hash_on_cookie: The cookie name to take the value from as hash input.
        Only required when `hash_on` or `hash_fallback` is set to `cookie`.
        If the specified cookie is not in the request, Kong will generate a value and set the cookie in the response.
        :param hash_on_cookie_path: The cookie path to set in the response headers.
        Only required when `hash_on` or `hash_fallback` is set to `cookie`.
        :param slots: The number of slots in the load balancer algorithm (10-65536)
        :param healthchecks: The configuration of health checking.
        :param tags: An optional set of strings associated with the Upstream, for grouping and filtering.
        :param host_header: The hostname to be used as `Host` header when proxying requests through Kong.
        """
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
        """ Update a upstream.

        :param url: A partial URL, e.g, '/upstreams/xxx_id'.
        :param kwargs: Data that will be updated.
        """
        body = {k: v for k, v in kwargs.items() if k in self.FIELDS}
        return super(UpstreamManager, self)._update(url=url, body=body)

    def update(self, upstream_id, **kwargs):
        """ Update a upstream by upstream_id.

        :param upstream_id: The unique identifier or the name of the Upstream to update.
        :param kwargs: Data that will be updated.
        """
        return self._update(url='/upstreams/%s' % upstream_id, **kwargs)

    def update_by_target(self, target_id, **kwargs):
        """ Update a upstream by target_id.

        :param target_id: The unique identifier or the host:port of
        the Target associated to the Upstream to be updated.
        """
        return self._update(url='/targets/%s/upstream' % target_id, **kwargs)

    def delete(self,  upstream_id):
        """ Delete a upstream by upstream_id.

        :param upstream_id: The unique identifier or the name of the Upstream to delete.
        """
        return self._delete(url='/upstreams/%s' % upstream_id)

    def delete_by_target(self, target_id):
        """ Delete a upstream by target_id.

        :param target_id: The unique identifier or the host:port of
        the Target associated to the Upstream to be deleted.
        """
        return self._delete(url='/targets/%s/upstream' % target_id)

    def add_target(self, upstream_id, target, weight=100, tags=None):
        """ Create a target associated to a specific upstream.

        :param upstream_id: The unique identifier or the name attribute of the Upstream
        that should be associated to the newly-created Target.
        :param target: The target address (ip or hostname) and port.
        If the hostname resolves to an SRV record, the port value will be
        overridden by the value from the DNS record.
        :param weight: The weight this target gets within the upstream load-balancer (0-1000).
        If the hostname resolves to an SRV record, the weight value will be
        overridden by the value from the DNS record.
        :param tags: An optional set of strings associated with the Target, for grouping and filtering.
        """
        body = {'target': target, 'weight': weight, 'tags': tags or [target]}
        return self._create(url='/upstreams/%s/targets' % upstream_id, body=body)

