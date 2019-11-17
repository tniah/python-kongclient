# -*- coding: utf-8 -*-
from kongclient.api import base


class SNIManager(base.Manager):
    """ Manager class for manipulating kong SNIs. """

    FIELDS = ('name', 'certificate', 'tags')

    def list(self, tags=None):
        """ Get a list of SNIs.

        :param tags: A string associated to SNIs in Kong, e.g, 'admin,example'
        """
        if tags:
            return self._list(url='/snis?tags=%s' % tags, response_key='data')
        return self._list(url='/snis', response_key='data')

    def get(self, sni_id):
        """ Get details of a SNI.

        :param sni_id: The unique identifier or the name of the SNI to retrieve.
        """
        return self._get(url='/snis/%s' % sni_id)

    def create(self, name, certificate_id, tags=None):
        """ Create a SNI

        :param certificate_id: The id (a UUID) of the certificate with which to associate the SNI hostname.
        :param name: The SNI name to associate with the given certificate.
        :param tags: An optional set of strings associated with the SNIs, for grouping and filtering.
        """
        body = {'name': name, 'certificate': {'id': certificate_id}, 'tags': tags or [name]}
        return self._create(url='/snis', body=body)

    def _update(self, url, **kwargs):
        """ Update a SNI.

        :param url: A partial URL, e.g, '/snis/xxx_id'.
        :param kwargs: Data that will be updated.
        """
        body = {k: v for k, v in kwargs.items() if k in self.FIELDS}
        if 'certificate' in body and body['certificate']:
            body['certificate'] = {'id': body['certificate']}
        return super(SNIManager, self)._update(url=url, body=body)

    def update(self, sni_id, **kwargs):
        """ Update a SNI by sni_id.

        :param sni_id: The unique identifier or the name of the SNI to update.
        :param kwargs: Data that will be updated.
        """
        return self._update(url='/snis/%s' % sni_id, **kwargs)

    def update_by_certificate(self, certificate_id, sni_id, **kwargs):
        """ Update a SNI by certificate_id.

        :param certificate_id: The unique identifier of the Certificate to update.
        :param sni_id: The unique identifier or the name of the SNI to update.
        :param kwargs: Data that will be updated.
        """
        return self._update(url='/certificates/%s/snis/%s' % (certificate_id, sni_id), **kwargs)

    def delete(self, sni_id):
        """ Delete a SNI by sni_id.

        :param sni_id: The unique identifier or the name of the SNI to delete.
        """
        return self._delete(url='/snis/%s' % sni_id)

    def delete_by_certificate(self, certificate_id, sni_id):
        """ Delete a SNI by certificate_id.

        :param certificate_id: The unique identifier of the Certificate to delete.
        :param sni_id: The unique identifier or the name of the SNI to delete.
        """
        return self._delete(url='/certificates/%s/snis/%s' % (certificate_id, sni_id))
