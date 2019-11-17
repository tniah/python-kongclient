# -*- coding: utf-8 -*-
from kongclient.api import base


class ConsumerManager(base.Manager):
    """ Manager class for manipulating kong consumers. """

    FIELDS = ('username', 'custom_id', 'tags')

    def list(self, tags=None):
        """ Get a list of consumers.

        :param tags: A string associated with Consumers, for filtering.
        """
        if tags:
            return self._list(url='/consumers?tags=%s' % tags, response_key='data')
        return self._list(url='/consumers', response_key='data')

    def list_plugins(self, consumer_id):
        """ Get a list of plugins associated to a specific consumer.

        :param consumer_id: The unique identifier or the name attribute
        of the Consumer whose Plugins are to be retrieved.
        """
        return self._list(url='/consumers/%s/plugins' % consumer_id, response_key='data')

    def get(self, consumer_id):
        """ Get details of a consumer.

        :param consumer_id: The unique identifier or the username of the Consumer to retrieve.
        """
        return self._get(url='/consumers/%s' % consumer_id)

    def get_plugin(self, consumer_id, plugin_id):
        """ Get a plugin associated to a specific consumer.

        :param consumer_id: The unique identifier or the username of the Consumer to retrieve.
        :param plugin_id: The unique identifier of the Plugin to retrieve.
        """
        return self._get(url='/consumers/%s/plugins/%s' % (consumer_id, plugin_id))

    def create(self, username, custom_id=None, tags=None):
        """ Create a consumer.

        :param username: The unique username of the consumer.
        You must send either this field or custom_id with the request.
        :param custom_id: Field for storing an existing unique ID for the
        consumer - useful for mapping Kong with users in your existing database.
        You must send either this field or username with the request.
        :param tags: An optional set of strings associated with the Consumer, for grouping and filtering.
        """
        body = {
            'username': username,
            'custom_id': custom_id,
            'tags': tags
        }
        return self._create(url='/consumers', body=body)

    def _update(self, url, **kwargs):
        """ Update a consumer.

        :param url: A partial URL, e.g, '/consumers/xxx_id'.
        :param kwargs: data that will be updated.
        """
        body = {k: v for k, v in kwargs.items() if k in self.FIELDS}
        return super(ConsumerManager, self)._update(url=url, body=body)

    def update(self, consumer_id, **kwargs):
        """ Update a consumer by consumer_id.

        :param consumer_id: The unique identifier or the username of the Consumer to update.
        :param kwargs: data that will be updated.
        """
        return self._update(url='/consumers/%s' % consumer_id, **kwargs)

    def update_by_plugin(self, plugin_id, **kwargs):
        """ Update a consumer by plugin_id.

        :param plugin_id: The unique identifier of the Plugin to update.
        :param kwargs: data that will be updated.
        """
        return self._update(url='/plugins/%s/consumer' % plugin_id, **kwargs)

    def delete(self, consumer_id):
        """ Delete a consumer by consumer_id.

        :param consumer_id: The unique identifier or the username of the Consumer to delete.
        """
        return self._delete(url='/consumers/%s' % consumer_id)

    def add_plugin(self, consumer_id, name, config=None, run_on='first',
                   protocols=('http', 'https'), enabled=True, tags=None):
        """ Create a plugin associated to a specific plugin.

        :param consumer_id: The unique identifier or the username attribute of the Consumer
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
        return self._create(url='/consumers/%s/plugins' % consumer_id, body=body)
