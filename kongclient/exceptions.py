# -*- coding: utf-8 -*-


class APIException(Exception):
    """ The API exception class for all http errors returned by Kong API.

    :param http_status: The http status code returned by the Kong API.
    :param message: The error message returned by the Kong API.
    :param method: The http method used to make request to the Kong API.
    :param url: The URL of the Kong API.
    """

    http_status = 500
    message = 'An unexpected error occurred'

    def __init__(self, http_status=None, message=None, method=None, url=None):
        self.http_status = http_status or self.__class__.http_status
        self.message = message or self.__class__.message
        self.method = method
        self.url = url

    def __str__(self):
        """ Return a string representing for http error. """
        formatted_string = '%s (Http %s)' % (self.message, self.http_status)
        if self.method:
            formatted_string += ' (Method %s)' % self.method
        if self.url:
            formatted_string += ' (Url %s)' % self.url
        return formatted_string
