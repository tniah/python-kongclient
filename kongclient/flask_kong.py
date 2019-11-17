# -*- coding: utf-8 -*-
from kongclient.kong_client import KongClient as _KongClient


class KongClient(_KongClient):

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app=app)

    def init_app(self, app):
        app.config.setdefault('KONG_ADMIN_URL', 'https://localhost:8444')
        app.config.setdefault('KONG_ADMIN_VERIFY_SSL', False)
        super(KongClient, self).__init__(
            kong_url=app.config['KONG_ADMIN_URL'],
            verify_ssl=app.config['KONG_ADMIN_VERIFY_SSL'])
