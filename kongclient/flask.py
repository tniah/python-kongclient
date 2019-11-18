# -*- coding: utf-8 -*-
from kongclient import client


class KongClient(client.KongClient):
    """ Kong class for the Python-Flask framework. """

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app=app)

    def init_app(self, app):
        # Configuration defaults
        app.config.setdefault('KONG_ADMIN_URL', 'https://localhost:8444')
        app.config.setdefault('KONG_ADMIN_VERIFY_SSL', False)
        super(KongClient, self).__init__(
            kong_url=app.config['KONG_ADMIN_URL'],
            verify_ssl=app.config['KONG_ADMIN_VERIFY_SSL'])
