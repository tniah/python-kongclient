# -*- coding: utf-8 -*-
from kongclient.api import base


class ACLManager(base.Manager):
    """ Manager class for manipulating kong acls. """

    FIELDS = ('name', 'hosts', 'protocols', 'methods', 'paths', 'headers',
              'https_redirect_status_code', 'regex_priority', 'strip_path',
              'preserve_host', 'snis', 'sources', 'destinations', 'service', 'tags')

    def list(self, tags=None):
        """ Get a list of all acls.

        :param tags: A string associated with ACLs, for filtering.
        """
        if tags:
            return self._list(url='/acls?tags=%s' % tags, response_key='data')
        return self._list(url='/acls', response_key='data')

    def get_consumer(self, acl_id):
        """ Get a consumer associated to a specific acl.

        :param acl_id: The unique identifier of the ACL to retrieve.
        """
        return self._get(url='/acls/%s/consumer' % (acl_id))
    
    def get_consumer_acls(self, consumer_id):
        """ Get acls associated to a specific consumer.

        :param consumer_id: The unique identifier or name of a consumer from which to
                            retrieve acls.
        """
        return self._get(url='/consumers/%s/acls' % (consumer_id))
