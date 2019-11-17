# -*- coding: utf-8 -*-
from kongclient.api import base


class NodeInfoManager(base.Manager):
    """ Manager class for manipulating kong node information. """

    def get_node_info(self):
        return self._get(url='/')

    def get_node_status(self):
        return self._get(url='/status')
