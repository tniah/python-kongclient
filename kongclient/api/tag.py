# -*- coding: utf-8 -*-
from kongclient.api import base


class TagManager(base.Manager):
    """ Manager class for manipulating kong tags. """

    def list(self):
        return self._list(url='/tags', response_key='data')

    def get(self, tag):
        return self._list(url='/tags/%s' % tag, response_key='data')
