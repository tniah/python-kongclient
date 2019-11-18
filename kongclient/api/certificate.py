# -*- coding: utf-8 -*-
from kongclient.api import base


class CertificateManager(base.Manager):
    """ Manager class for manipulating kong certificates. """

    FIELDS = ('cert', 'key', 'tags', 'snis')

    def list(self, tags):
        """ Get a list of all certificates.

        :param tags: A string associated to certificates in Kong, e.g, 'admin,example'
        """
        if tags:
            return self._list(url='/certificates?tags=%s' % tags, response_key='data')
        return self._list(url='/certificates', response_key='data')

    def list_services(self, certificate_id):
        """ Get a list of services associated to a specific certificate.

        :param certificate_id: The unique identifier of the Certificate
        whose Services are to be retrieved.
        """
        return self._list(url='/certificates/%s/services' % certificate_id, response_key='data')

    def list_snis(self, certificate_id):
        """ Get a list of snis associated to a specific certificate.

        :param certificate_id: The unique identifier of the Certificate
        whose SNIs are to be retrieved.
        """
        return self._list(url='/certificates/%s/snis' % certificate_id, response_key='data')

    def get(self, certificate_id):
        """ Get details of a certificate.

        :param certificate_id: The unique identifier of the Certificate to retrieve.
        """
        return self._get(url='/certificates/%s' % certificate_id)

    def get_service(self, certificate_id, service_id):
        """ Get a service associated to a specific certificate.

        :param certificate_id: The unique identifier of the Certificate to retrieve.
        :param service_id: The unique identifier or the name of the Service to retrieve.
        """
        return self._get(url='/certificates/%s/services/%s' % (certificate_id, service_id))

    def get_sni(self, certificate_id, sni_id):
        """ Get a sni associated to a specific certificate.

        :param certificate_id: The unique identifier of the Certificate to retrieve.
        :param sni_id: The unique identifier of the SNI to retrieve.
        """
        return self._get(url='/certificates/%s/snis/%s' % (certificate_id, sni_id))

    def create(self, cert, key, snis=None, tags=None):
        """ Create a certificate.

        :param cert: PEM-encoded public certificate chain of the SSL key pair.
        :param key: PEM-encoded private key of the SSL key pair.
        :param snis: An array of zero or more hostnames to associate with this certificate as SNIs.
        :param tags: An optional set of strings associated with the Certificate, for grouping and filtering.
        """
        body = {'cert': cert, 'key': key, 'snis': snis, 'tags': tags}
        return self._create(url='/certificates', body=body)

    def update(self, certificate_id, **kwargs):
        """ Update a certificate by certificate_id.

        :param certificate_id: The unique identifier of the Certificate to update.
        :param kwargs: data that will be updated.
        """
        body = {k: v for k, v in kwargs.items() if k in self.FIELDS}
        return self._update(url='/certificates/%s' % certificate_id, body=body)

    def delete(self, certificate_id):
        """ Delete a certificate by certificate_id.

        :param certificate_id: The unique identifier of the Certificate to delete.
        """
        return self._delete(url='/certificates/%s' % certificate_id)

    def add_service(self, certificate_id, name, url=None, protocol='http', host=None, port=80, path=None,
                    retries=5, connect_timeout=60000, write_timeout=60000, read_timeout=60000, tags=None):
        """ Create a service associated to a specific service.

        :param certificate_id: The unique identifier of the Certificate
        that should be associated to the newly-created Service.
        :param name: The service name.
        :param protocol: The protocol used to communicate with the upstream.
        :param host: The host of the upstream server.
        :param port: The upstream server port.
        :param path: The path to be used in requests to the upstream server.
        :param url: Shorthand attribute to set protocol, host, port and path at once.
        :param retries: The number of retries to execute upon failure to proxy.
        :param connect_timeout: The timeout in milliseconds for establishing
        a connection to the upstream server.
        :param write_timeout: The timeout in milliseconds between two successive
        write operations for transmitting a request to the upstream server.
        :param read_timeout: The timeout in milliseconds between two successive
        read operations for transmitting a request to the upstream server.
        :param tags: An optional set of strings associated with the Service,
        for grouping and filtering.
        """
        body = {
            'name': name,
            'retries': retries,
            'connect_timeout': connect_timeout,
            'write_timeout': write_timeout,
            'read_timeout': read_timeout,
            'tags': tags or [name]
        }
        if not url:
            body.update({'protocol': protocol, 'host': host, 'port': port, 'path': path})
        else:
            body['url'] = url
        return self._create(url='/certificates/%s/services' % certificate_id, body=body)

    def add_sni(self, certificate_id, name, tags=None):
        """ Create a SNI associated to a specific service.

        :param certificate_id: The unique identifier of the Certificate
        that should be associated to the newly-created SNI.
        :param name: The SNI name to associate with the given certificate.
        :param tags: An optional set of strings associated with the SNIs, for grouping and filtering.
        """
        body = {'name': name, 'tags': tags or [name]}
        return self._create(url='/certificates/%s/snis' % certificate_id, body=body)
