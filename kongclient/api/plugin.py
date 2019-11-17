# -*- coding: utf-8 -*-
from kongclient.api import base


class PluginManager(base.Manager):
    """ Manager class for manipulating kong plugins. """

    FIELDS = ('name', 'route', 'service', 'consumer',
              'config', 'run_on', 'protocols', 'enabled', 'tags')

    def list(self, tags=None):
        """ Get a list of plugins.

        :param tags: A string associated with Plugins, for filtering.
        """
        if tags:
            return self._list(url='/plugins?tags=%s' % tags, response_key='data')
        return self._list(url='/plugins', response_key='data')

    def get(self, plugin_id):
        """ Get details of a plugin.

        :param plugin_id: The unique identifier of Plugin to retrieve.
        """
        return self._get(url='/plugins/%s' % plugin_id)

    def get_enabled_plugins(self):
        """ Get a list of all installed plugins on the Kong node. """
        return self._get(url='/plugins/enabled')

    def get_schema(self, plugin_id):
        """ Get the schema of a plugin’s configuration.

        :param plugin_id: The unique identifier of Plugin to retrieve.
        """
        return self._get(url='/plugins/schema/%s' % plugin_id)

    def get_service(self, plugin_id):
        """ Get a service associated to a specific plugin.

        :param plugin_id: The unique identifier of Plugin to retrieve.
        """
        return self._get(url='/plugins/%s/service' % plugin_id)

    def get_route(self, plugin_id):
        """ Get a route associated to a specific plugin.

        :param plugin_id: The unique identifier of Plugin to retrieve.
        """
        return self._get(url='/plugins/%s/route' % plugin_id)

    def get_consumer(self, plugin_id):
        """ Get a consumer associated to a specific plugin.

        :param plugin_id: The unique identifier of Plugin to retrieve.
        """
        return self._get(url='/plugins/%s/consumer' % plugin_id)

    def create(self, name, route_id=None, service_id=None, consumer_id=None, config=None,
               run_on='first', protocols=('http', 'https'), enabled=True, tags=None):
        """ Create a plugin.

        :param name: The name of the Plugin that’s going to be added.
        :param route_id: The unique identifier of the Route that should be
        associated to the newly-created Plugin.
        :param service_id: The unique identifier of the Service that should be
        associated to the newly-created Plugin.
        :param consumer_id: The unique identifier of the Consumer that should be
        associated to the newly-created Plugin.
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
        """ Update a plugin.

        :param url: A partial URL, e.g, '/plugins/xxx_id'.
        :param kwargs: data that will be updated.
        """
        body = {k: v for k, v in kwargs.items() if k in self.FIELDS}
        if 'route' in body and body['route']:
            body['route'] = {'id': body['route']}
        if 'service' in body and body['service']:
            body['service'] = {'id': body['service']}
        if 'consumer' in body and body['consumer']:
            body['consumer'] = {'id': body['consumer']}
        return super(PluginManager, self)._update(url=url, body=body)

    def update(self, plugin_id, **kwargs):
        """ Update a plugin by plugin_id.

        :param plugin_id: The unique identifier of the Plugin to update.
        :param kwargs: data will be updated.
        """
        return self._update(url='/plugins/%s' % plugin_id, **kwargs)

    def update_by_route(self, route_id, plugin_id, **kwargs):
        """ Update a plugin by route_id.

        :param route_id: The unique identifier or the name of the Route to update.
        :param plugin_id: The unique identifier of the Plugin to update.
        :param kwargs: data will be updated.
        """
        return self._update(url='/routes/%s/plugins/%s' % (route_id, plugin_id), **kwargs)

    def update_by_service(self, service_id, plugin_id, **kwargs):
        """ Update a plugin by service_id.

        :param service_id: The unique identifier or the name of the Service to update.
        :param plugin_id: The unique identifier of the Plugin to update.
        :param kwargs: data will be updated.
        """
        return self._update(url='/services/%s/plugins/%s' % (service_id, plugin_id), **kwargs)

    def update_by_consumer(self, consumer_id, plugin_id, **kwargs):
        """ Update a plugin by consumer_id.

        :param consumer_id: The unique identifier or the name of the Consumer to update.
        :param plugin_id: The unique identifier of the Plugin to update.
        :param kwargs: data will be updated.
        """
        return self._update(url='/consumers/%s/plugins/%s' % (consumer_id, plugin_id), **kwargs)

    def delete(self, plugin_id):
        """ Delete a plugin by plugin_id.

        :param plugin_id: The unique identifier of the Plugin to delete.
        """
        return self._delete(url='/plugins/%s' % plugin_id)

    def delete_by_route(self, route_id, plugin_id):
        """ Delete a plugin by route_id.

        :param route_id: The unique identifier or the name of the Route to delete.
        :param plugin_id: The unique identifier of the Plugin to delete.
        """
        return self._delete(url='/routes/%s/plugins/%s' % (route_id, plugin_id))

    def delete_by_service(self, service_id, plugin_id):
        """ Delete a plugin by service_id.

        :param service_id: The unique identifier or the name of the Service to delete.
        :param plugin_id: The unique identifier of the Plugin to delete.
        """
        return self._delete(url='/services/%s/plugins/%s' % (service_id, plugin_id))

    def delete_by_consumer(self, consumer_id, plugin_id):
        """ Delete a plugin by consumer_id.

        :param consumer_id: The unique identifier or the name of the Consumer to delete.
        :param plugin_id: The unique identifier of the Plugin to delete.
        """
        return self._delete(url='/consumers/%s/plugins/%s' % (consumer_id, plugin_id))
