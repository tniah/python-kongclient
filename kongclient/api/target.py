# -*- coding: utf-8 -*-
from kongclient.api import base


class TargetManager(base.Manager):
    """ Manager class for manipulating kong targets. """

    def get_upstream(self, target_id):
        return self._get(url='/targets/%s/upstream' % target_id)

    def set_healthy_address_by_upstream(self, upstream_id, target_id, address):
        return self._set(url='/upstreams/%s/targets/%s/%s/healthy' % (upstream_id, target_id, address))

    def set_healthy_target_by_upstream(self, upstream_id, target_id):
        return self._set(url='/upstreams/%s/targets/%s/healthy' % (upstream_id, target_id))

    def set_unhealthy_target_by_upstream(self, upstream_id, target_id):
        return self._set(url='/upstreams/%s/targets/%s/unhealthy' % (upstream_id, target_id))

    def delete_target_by_upstream(self, upstream_id, target_id):
        return self._delete(url='/upstreams/%s/targets/%s' % (upstream_id, target_id))
