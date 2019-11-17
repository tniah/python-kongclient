# -*- coding: utf-8 -*-
from kongclient.api import base


class NodeInfoManager(base.Manager):
    """ Manager class for manipulating Kong node information. """

    def get_node_info(self):
        """ Retrieve generic details about a node. """
        return self._get(url='/')

    def get_node_status(self):
        """ Retrieve node status. """
        return self._get(url='/status')
