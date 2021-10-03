import datetime
import json

from flask import Response


class APIResponse(Response):
    default_mimetype = 'application/json'

    def __init__(self, params = {}, status = 'success'):
        def date_converter(value):
            if isinstance(value, (datetime.date, datetime.datetime, datetime.time)):
                return value.__str__()
        data = {'status': status, **params}
        super().__init__(json.dumps(data, default=date_converter))

    @classmethod
    def force_type(cls, rv, environ=None):
        def converter(k):
            if isinstance(k, (datetime.date, datetime.datetime, datetime.time)):
                return k.__str__()

        if isinstance(rv, dict):
            rv = json.dumps(rv, default=converter)
        return super(APIResponse, cls).force_type(rv, environ)


class APIError(APIResponse):
    def __init__(self, errors):
        super().__init__({'errors': errors}, 'error')

