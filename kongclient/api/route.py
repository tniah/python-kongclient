# -*- coding: utf-8 -*-
from kongclient.api import base


class RouteManager(base.Manager):
    """ Manager class for manipulating kong routes. """

    FIELDS = ('name', 'hosts', 'protocols', 'methods', 'paths', 'headers',
              'https_redirect_status_code', 'regex_priority', 'strip_path',
              'preserve_host', 'snis', 'sources', 'destinations', 'service', 'tags')

    def list(self, tags=None):
        """ Get a list of all routes.

        :param tags: A string associated with Routes, for filtering.
        """
        if tags:
            return self._list(url='/routes?tags=%s' % tags, response_key='data')
        return self._list(url='/routes', response_key='data')

    def list_plugins(self, route_id):
        """ Get a list of plugins associated to a specific route.

        :param route_id: The unique identifier or the name attribute
        of the Route whose Plugins are to be retrieved.
        """
        return self._list(url='/routes/%s/plugins' % route_id, response_key='data')

    def get(self, route_id):
        """ Get details of a route.

        :param route_id: The unique identifier or the name of the Route to retrieve.
        """
        return self._get(url='/routes/%s' % route_id)

    def get_service(self, route_id):
        """ Get a service associated to a specific route.

        :param route_id: The unique identifier or the name of the Route to retrieve.
        """
        return self._get(url='/routes/%s/service' % route_id)

    def get_plugin(self, route_id, plugin_id):
        """ Get a plugin associated to a specific route.

        :param route_id: The unique identifier or the name of the Route to retrieve.
        :param plugin_id: The unique identifier or the name of the Plugin to retrieve.
        """
        return self._get(url='/routes/%s/plugins/%s' % (route_id, plugin_id))

    def create(self, name, hosts=None, service_id=None, protocols=('http', 'https'), headers=None,
               methods=('GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS', 'HEAD'), paths=None,
               https_redirect_status_code=426, regex_priority=0, strip_path=False, preserve_host=True,
               snis=None, sources=None, destinations=None, tags=None):
        """ Create a route.

        :param name: The name of the Route.
        :param hosts: A list of domain names that match this Route.
        :param service_id: The unique identifier of the Service that this Route is associated to.
        :param protocols: A list of the protocols this Route should allow.
        :param headers: One or more lists of values indexed by header name
        that will cause this Route to match if present in the request.
        :param methods: A list of HTTP methods that match this Route.
        :param paths: A list of paths that match this Route.
        :param https_redirect_status_code: The status code Kong responds with when all properties
        of a Route match except the protocol i.e. if the protocol of the request is HTTP instead of HTTPS.
        :param regex_priority: A number used to choose which route resolves a given request
        when several routes match it using regexes simultaneously.
        :param strip_path: When matching a Route via one of the paths,
        strip the matching prefix from the upstream request URL.
        :param preserve_host: When matching a Route via one of the hosts domain names,
        use the request Host header in the upstream request headers.
        If set to False, the upstream Host header will be that of the Service’s host.
        :param snis: A list of SNIs that match this Route when using stream routing.
        :param sources: A list of IP sources of incoming connections that match
        this Route when using stream routing. Each entry is an object with fields “ip”
        (optionally in CIDR range notation) and/or “port”.
        :param destinations: A list of IP destinations of incoming connections that match
        this Route when using stream routing. Each entry is an object with fields “ip”
        (optionally in CIDR range notation) and/or “port”.
        :param tags: An optional set of strings associated with the Route, for grouping and filtering.
        """
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
        if service_id:
            body['service'] = {'id': service_id}
        return self._create(url='/routes', body=body)

    def _update(self, url, **kwargs):
        """ Update a route.

        :param url: a partial URL, e.g, '/routes/xxx_id'.
        :param kwargs: data that will be updated.
        """
        body = {k: v for k, v in kwargs.items() if k in self.FIELDS}
        if 'service' in body and body['service']:
            body['service'] = {'id': body['service']}
        return super(RouteManager, self)._update(url=url, body=body)

    def update(self, route_id, **kwargs):
        """ Update a route by route_id.

        :param route_id: The unique identifier or the name of the Route to update.
        :param kwargs: data that will be updated.
        """
        return self._update(url='/routes/%s' % route_id, **kwargs)

    def update_by_service(self, service_id, route_id, **kwargs):
        """ Update a route by service_id.

        :param service_id: The unique identifier or the name of the Service to update.
        :param route_id: The unique identifier or the name of the Route to update.
        :param kwargs: data that will be updated.
        """
        return self._update(url='/services/%s/routes/%s' % (service_id, route_id), **kwargs)

    def update_by_plugin(self, plugin_id, **kwargs):
        """ Update a route by plugin_id.

        :param plugin_id: The unique identifier or the name of the Plugin to update.
        :param kwargs: data that will be updated.
        """
        return self._update(url='/plugins/%s/route' % plugin_id, **kwargs)

    def delete(self, route_id):
        """ Delete a route by route_id.

        :param route_id: The unique identifier or the name of the Route to delete.
        """
        return self._delete(url='/routes/%s' % route_id)

    def delete_by_service(self, service_id, route_id):
        """ Delete a route by service_id.

        :param service_id: The unique identifier or the name of the Service to delete.
        :param route_id: The unique identifier or the name of the Route to delete.
        """
        return self._delete(url='/services/%s/routes/%s' % (service_id, route_id))

    def add_plugin(self, route_id, name, config=None, run_on='first',
                   protocols=('http', 'https'), enabled=True, tags=None):
        """ Create a plugin associated to a specific route.

        :param route_id: The unique identifier of the Route that should be
        associated to the newly-created Plugin.
        :param name: The name of the Plugin that’s going to be added.
        :param config: The configuration properties for the Plugin
        which can be found on the plugins documentation page in the Kong Hub.
        :param run_on: Control on which Kong nodes this plugin will run.
        :param protocols: A list of the request protocols that will trigger this plugin.
        :param enabled: Whether the plugin is applied.
        :param tags: An optional set of strings associated with the Plugin, for grouping and filtering.
        """
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
