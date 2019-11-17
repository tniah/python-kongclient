# -*- coding: utf-8 -*-
from kongclient.api import base


class ServiceManager(base.Manager):
    """ Manager class for manipulating kong services. """

    FIELDS = ('name', 'protocol', 'host', 'port', 'path', 'url', 'retries',
              'connect_timeout', 'write_timeout', 'read_timeout', 'client_certificate', 'tags')

    def list(self, tags=None):
        """ Get a list of all services.

        :param tags: A string associated to services in Kong, e.g, 'admin,example'
        """
        if tags:
            return self._list(url='/services?tags=%s' % tags, response_key='data')
        return self._list(url='/services', response_key='data')

    def list_routes(self, service_id):
        """ Get a list of routes associated to a specific service.

        :param service_id: The unique identifier or the name attribute
        of the Service whose Routes are to be retrieved.
        """
        return self._list(url='/services/%s/routes' % service_id, response_key='data')

    def list_plugins(self, service_id):
        """ Get a list of plugins associated to a specific service.

        :param service_id: The unique identifier or the name attribute
        of the Service whose Plugins are to be retrieved.
        """
        return self._list(url='/services/%s/plugins' % service_id, response_key='data')

    def get(self, service_id):
        """ Get details of a service.

        :param service_id: The unique identifier or the name of the Service to retrieve.
        """
        return self._get(url='/services/%s' % service_id)

    def get_route(self, service_id, route_id):
        """ Get a route associated to a specific service.

        :param service_id: The unique identifier or the name of the Service to retrieve.
        :param route_id: The unique identifier or the name of the Route to retrieve.
        """
        return self._get(url='/services/%s/routes/%s' % (service_id, route_id))

    def get_plugin(self, service_id, plugin_id):
        """ Get a plugin associated to a specific service.

        :param service_id: The unique identifier or the name of the Service to retrieve.
        :param plugin_id: The unique identifier or the name of the Plugin to retrieve.
        """
        return self._get(url='/services/%s/plugins/%s' % (service_id, plugin_id))

    def create(self, name, url=None, protocol='http', host=None, port=80, path=None,
               retries=5, connect_timeout=60000, write_timeout=60000, read_timeout=60000,
               client_certificate=None, tags=None):
        """ Create a service.

        :param name: The service name.
        :param protocol: The protocol used to communicate with the upstream.
        :param host: The host of the upstream server.
        :param port: The upstream server port.
        :param path: The path to be used in requests to the upstream server.
        :param url: Shorthand attribute to set protocol, host, port and path at once.
        :param retries: The number of retries to execute upon failure to proxy.
        :param connect_timeout: The timeout in milliseconds for establishing
        a connection to the upstream server.
        :param write_timeout: The timeout in milliseconds between two successive
        write operations for transmitting a request to the upstream server.
        :param read_timeout: The timeout in milliseconds between two successive
        read operations for transmitting a request to the upstream server.
        :param client_certificate: Certificate to be used as client certificate
        while TLS handshaking to the upstream server.
        :param tags: An optional set of strings associated with the Service,
        for grouping and filtering.
        """
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

    def _update(self, url, **kwargs):
        """ Update a service.

        :param url: a partial URL, e.g, '/services/xxx_id'
        :param kwargs: data that will be updated.
        """
        body = {k: v for k, v in kwargs.items() if k in self.FIELDS}
        if 'client_certificate' in body and body['client_certificate']:
            body['client_certificate'] = {'id': body['client_certificate']}
        return super(ServiceManager, self)._update(url=url, body=body)

    def update(self, service_id, **kwargs):
        """ Update a service by service_id.

        :param service_id: The unique identifier or the name of the Service to update.
        :param kwargs: data that will be updated.
        """
        return self._update(url='/services/%s' % service_id, **kwargs)

    def update_by_route(self, route_id, **kwargs):
        """ Update a service by route_id.

        :param route_id: The unique identifier or the name of the Route
        associated to the Service to be updated.
        :param kwargs: data that will be updated.
        """
        return self._update(url='/routes/%s/service' % route_id, **kwargs)

    def update_by_plugin(self, plugin_id, **kwargs):
        """ Update a service by plugin_id.

        :param plugin_id: The unique identifier of the Plugin
        associated to the Service to be updated.
        :param kwargs: data that will be updated.
        """
        return self._update(url='/plugins/%s/service' % plugin_id, **kwargs)

    def update_by_certificate(self, certificate_id, service_id, **kwargs):
        """ Update a service by certificate_id.

        :param certificate_id: The unique identifier of the Certificate
        associated to the Service to be updated.
        :param service_id: The unique identifier or the name of the Service to update.
        :param kwargs: data that will be updated.
        """
        return self._update(url='/certificates/%s/services/%s' % (certificate_id, service_id), **kwargs)

    def delete(self, service_id):
        """ Delete a service by service_id.

        :param service_id: The unique identifier or the name of the Service to delete.
        """
        return self._delete(url='/services/%s' % service_id)

    def delete_by_route(self, route_id):
        """ Delete a service by route_id.

        :param route_id: The unique identifier or the name of the Route
        associated to the Service to be deleted.
        """
        return self._delete(url='/routes/%s/service' % route_id)

    def delete_by_certificate(self, certificate_id, service_id):
        """ Delete a service by certificate_id.

        :param certificate_id: The unique identifier of the Certificate
        associated to the Service to be deleted.
        :param service_id: The unique identifier or the name of the Service to delete.
        """
        return self._delete(url='/certificates/%s/services/%s' % (certificate_id, service_id))

    def add_route(self, service_id, name, hosts, protocols=('http', 'https'), headers=None,
                  methods=('GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS', 'HEAD'), paths=None,
                  https_redirect_status_code=426, regex_priority=0, strip_path=False, preserve_host=True,
                  snis=None, sources=None, destinations=None, tags=None):
        """ Create a route associated to a specific service.

        :param service_id: The unique identifier or the name attribute of the Service
        that should be associated to the newly-created Route.
        :param name: The name of the Route.
        :param hosts: A list of domain names that match this Route.
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
        return self._create(url='/services/%s/routes' % service_id, body=body)

    def add_plugin(self, service_id, name, config=None, run_on='first',
                   protocols=('http', 'https'), enabled=True, tags=None):
        """ Create a route associated to a specific service.

        :param service_id: The unique identifier or the name attribute of the Service
        that should be associated to the newly-created Plugin.
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
        return self._create(url='/services/%s/plugins' % service_id, body=body)
