""" httplib2 for source address """

import http.client
import httplib2

class HTTPConnection(http.client.HTTPConnection):
    def __init__(self, *args, proxy_info=None, **kwargs):
        super().__init__(*args, **kwargs)

class HTTPSConnection(http.client.HTTPSConnection):
    def __init__(self, *args, proxy_info=None, **kwargs):
        super().__init__(*args, **kwargs)

httplib2.SCHEME_TO_CONNECTION.update({
    "http": HTTPConnection,
    "https": HTTPSConnection
})

class Connections:
    def __init__(self, http):
        self.http = http
        self.connections = {}

    def get(self, key):
        return self.connections.get(key)

    def __setitem__(self, key, connection):
        if isinstance(connection, (HTTPConnection, HTTPSConnection)):
            connection.source_address = self.http.source_address
        self.connections[key] = connection
    
    def __getitem__(self, key):
        return self.connections.get(key)

class Http(httplib2.Http):
    def __init__(self, source_address, *args, **kwargs):
        super(Http, self).__init__(*args, **kwargs)
        self.source_address = source_address
        self.connections = Connections(self)