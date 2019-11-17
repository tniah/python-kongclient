# -*- coding: utf-8 -*-
from kongclient.api import base


class TargetManager(base.Manager):
    """ Manager class for manipulating kong targets. """

    def get_upstream(self, target_id):
        """ Get a upstream associated to a specific target.

        :param target_id: The host/port combination element of the target to retrieve,
        or the id of an existing target entry.
        """
        return self._get(url='/targets/%s/upstream' % target_id)

    def set_healthy_address_by_upstream(self, upstream_id, target_id, address):
        """ Set target address as healthy.

        :param upstream_id: The unique identifier or the name of the upstream.
        :param target_id: The host/port combination element of the target to set as healthy,
        or the `id` of an existing target entry.
        :param address: The host/port combination element of the address to set as healthy.
        """
        return self._set(url='/upstreams/%s/targets/%s/%s/healthy' % (upstream_id, target_id, address))

    def set_healthy_target_by_upstream(self, upstream_id, target_id):
        """ Set target as healthy.

        :param upstream_id: The unique identifier or the name of the upstream.
        :param target_id: The host/port combination element of the target to set as healthy,
        or the `id` of an existing target entry.
        """
        return self._set(url='/upstreams/%s/targets/%s/healthy' % (upstream_id, target_id))

    def set_unhealthy_target_by_upstream(self, upstream_id, target_id):
        """ Set target as unhealthy.

        :param upstream_id: The unique identifier or the name of the upstream.
        :param target_id: The host/port combination element of the target to set as unhealthy,
        or the `id` of an existing target entry.
        """
        return self._set(url='/upstreams/%s/targets/%s/unhealthy' % (upstream_id, target_id))

    def delete_target_by_upstream(self, upstream_id, target_id):
        """ Delete target by upstream_id.

        :param upstream_id: The unique identifier or the name of the upstream
        for which to delete the target.
        :param target_id: The host:port combination element of the target to remove,
        or the `id` of an existing target entry.
        """
        return self._delete(url='/upstreams/%s/targets/%s' % (upstream_id, target_id))
