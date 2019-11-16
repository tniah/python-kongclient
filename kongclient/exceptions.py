# -*- coding: utf-8 -*-


class APIException(Exception):

    http_status = 500
    message = 'An unexpected error occurred'

    def __init__(self, http_status=None, message=None, method=None, url=None):

        self.http_status = http_status or self.__class__.http_status
        self.message = message or self.__class__.message
        self.method = method
        self.url = url

    def __str__(self):

        formatted_string = '%s (Http %s)' % (self.message, self.http_status)
        if self.method:
            formatted_string += ' (Method %s)' % self.method
        if self.url:
            formatted_string += ' (Url %s)' % self.url
