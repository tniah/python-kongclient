# -*- coding: utf-8 -*-
from kongclient.api import base


class TagManager(base.Manager):
    """ Manager class for manipulating kong tags. """

    def list(self):
        """ Get a list of all tags. """
        return self._list(url='/tags', response_key='data')

    def get(self, tag):
        """ Get a list of entities with the specified tag.

        :param tag: A string associated with entities, e.g, 'user-level'
        """
        return self._list(url='/tags/%s' % tag, response_key='data')
