import httplib2
import re
import urllib
try:
    import simplejson as json
except:
    import json
from endpoints_v1_1 import mapping_table as mapping_table_v1_1
try:
    from google.appengine.api.urlfetch_errors import InternalTransientError
except ImportError:
    class InternalTransientError(Exception):
        pass


TWITTER_BASE_URL = 'https://api.twitter.com'
DEFAULT_HTTP_METHOD = 'GET'
DEFAULT_HTTP_STATUS_CODE = 200
DEFAULT_CONTENT_TYPE = 'application/x-www-form-urlencoded'


class TwitterError(Exception):

    def __init__(self, msg, error_code=None):
        self.msg = msg
        self.error_code = error_code

    def __str__(self):
        return repr('%s: %s' % (self.error_code, self.msg))


def clean_kwargs(kwargs):
    for key, value in kwargs.iteritems():
        if hasattr(value, '__iter__'):
            kwargs[key] = ','.join(map(str, value))
#    underscore_keys = [key for key in kwargs if key.find('_')>=0]
#    for key in underscore_keys:
#        val = kwargs.pop(key)
#        kwargs[key.replace('_','-')] = val


class Twitter(object):

    def __init__(self, token=None, api_version=1.1, client_args=None, client=None):
        self.token = token
        if api_version == 1.1:
            self.mapping_table=mapping_table_v1_1
        else:
            raise ValueError("Unsupported Twitter API Version: %d" %
                    api_version)
        if client_args is None:
            client_args = {}
        if client is None:
            self.client = httplib2.Http(**client_args)
        else:
            self.client = client

    def __getattr__(self, api_call):
        def call(self, **kwargs):
            api_map = self.mapping_table[api_call]
            path = self.mapping_table.get('path_prefix','') + api_map.get('path','')
            method = api_map.get('method', DEFAULT_HTTP_METHOD)
            status = api_map.get('status', DEFAULT_HTTP_STATUS_CODE)
            valid_params = api_map.get('valid_params', [])
            body = kwargs.pop('data', None)
            url = re.sub(
                    '\{\{(?P<m>[a-zA-Z_]+)\}\}',
                    lambda m: "%s" % urllib.quote(str(kwargs.pop(m.group(1),''))),
                    TWITTER_BASE_URL + path
            )
            clean_kwargs(kwargs)
            for kw in kwargs:
                if kw not in valid_params:
                    raise TypeError("%s() got an unexpected keyword argument "
                            "'%s'" % (api_call, kw))
            url += '?' + urllib.urlencode(kwargs)
            return self._make_request(method, url, body, status)
        return call.__get__(self)

    def _make_request(self, method, url, body, status):
        headers = {}
        if self.token:
            headers["Authorization"] = "Bearer %s" % self.token
        if body:
            content_type = self.mapping_table.get('content_type', DEFAULT_CONTENT_TYPE)
            headers["Content-Type"] = content_type
            if isinstance(body, dict):
                if content_type == 'application/x-www-form-urlencoded':
                    body = urllib.urlencode(body)
                elif content_type == 'application/json':
                    body = json.dumps(body)
        else:
            body = ''
        try:
            response,content = self.client.request(url, method=method, body=body,
                    headers=headers)
        except InternalTransientError as e:
            response,content = self.client.request(url, method=method, body=body,
                    headers=headers)
        return self._response_handler(response, content, status)

    def _response_handler(self, response, content, status):
        if not response:
            raise TwitterError('Response Not Found')
        response_status = int(response.get('status', 0))
        if response_status != status:
            raise TwitterError(content, response_status)
        if response.get('location'):
            return response.get('location')
        elif content.strip():
            return json.loads(content)
        else:
            return responses[response_status]
