# -*- coding: utf-8 -*-
import requests
from requests.compat import urljoin
from kongclient import api


class SessionClient(requests.Session):

    def __init__(self, base_url, verify_ssl=False):

        super(SessionClient, self).__init__()
        self.verify = bool(verify_ssl)
        self.base_url = base_url

    def request(self, method, url, *args, **kwargs):

        url = urljoin(base=self.base_url, url=url)
        return super(SessionClient, self).request(method, url, *args, **kwargs)


class Client:

    def __init__(self, kong_url, verify_ssl=True):

        self.client = SessionClient(base_url=kong_url, verify_ssl=verify_ssl)
        self.services = api.ServiceManager(self)
        self.routes = api.RouteManager(self)
        self.consumers = api.ConsumerManager(self)
        self.plugins = api.PluginManager(self)
        self.certificates = api.CertificateManager(self)
        self.snis = api.SNIManager(self)
        self.upstreams = api.UpstreamManager(self)
        self.targets = api.TargetManager(self)
        self.tags = api.TagManager(self)
        self.info = api.NodeInfoManager(self)
