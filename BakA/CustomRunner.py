# -*- coding: utf-8 -*-
from autobahn.twisted import websocket
from autobahn.twisted.websocket import WampWebSocketClientFactory
from autobahn.wamp.types import ComponentConfig
from autobahn.websocket.protocol import parseWsUrl
import sys
from twisted.python import log

from CustomFactory import CustomFactory

class CustomRunner:
    """
    This class is a convenience tool mainly for development and quick hosting
    of WAMP application components.

    It can host a WAMP application component in a WAMP-over-WebSocket client
    connecting to a WAMP router.
    """

    def __init__(self, url, realm, extra=None, debug=False, debug_wamp=False, debug_app=False):
        """

        :param url: The WebSocket URL of the WAMP router to connect to (e.g. `ws://somehost.com:8090/somepath`)
        :type url: unicode
        :param realm: The WAMP realm to join the application session to.
        :type realm: unicode
        :param extra: Optional extra configuration to forward to the application component.
        :type extra: dict
        :param debug: Turn on low-level debugging.
        :type debug: bool
        :param debug_wamp: Turn on WAMP-level debugging.
        :type debug_wamp: bool
        :param debug_app: Turn on app-level debugging.
        :type debug_app: bool
        """
        self.url = url
        self.realm = realm
        self.extra = extra or dict()
        self.debug = debug
        self.debug_wamp = debug_wamp
        self.debug_app = debug_app
        self.make = None

    def run(self, make, start_reactor=True):
        """
        Run the application component.

        :param make: A factory that produces instances of :class:`autobahn.asyncio.wamp.ApplicationSession`
           when called with an instance of :class:`autobahn.wamp.types.ComponentConfig`.
        :type make: callable
        """
        from twisted.internet import reactor

        isSecure, host, port, resource, path, params = parseWsUrl(self.url)

        # start logging to console
        if self.debug or self.debug_wamp or self.debug_app:
            log.startLogging(sys.stdout)

        # factory for use ApplicationSession
        def create():
            cfg = ComponentConfig(self.realm, self.extra)
            try:
                session = make(cfg)
            except Exception:
                # the app component could not be created .. fatal
                log.err()
                reactor.stop()
            else:
                session.debug_app = self.debug_app
                return session

        # create a WAMP-over-WebSocket transport client factory
        transport_factory = CustomFactory(create, url=self.url,
                                                       debug=self.debug, debug_wamp=self.debug_wamp)
        transport_factory.bob = self
        # start the client from a Twisted endpoint
        """from twisted.internet.endpoints import clientFromString

        if isSecure:
            endpoint_descriptor = "ssl:{0}:{1}".format(host, port)
        else:
            endpoint_descriptor = "tcp:{0}:{1}".format(host, port)

        client = clientFromString(reactor, endpoint_descriptor)
        d = client.connect(transport_factory)"""

        #transport_factory.host = host
        #transport_factory.port = port
        #transport_factory.isSecure = isSecure
        #transport_factory.url
        websocket.connectWS(transport_factory)


        # if an error happens on the connect(), we save the underlying
        # exception so that after the event-loop exits we can re-raise
        # it to the caller.

        class ErrorCollector:
            exception = None

            def __call__(self, failure):
                self.exception = failure.value
                # print(failure.getErrorMessage())
                reactor.stop()
        connect_error = ErrorCollector()
        #d.addErrback(connect_error)

        # now enter the Twisted reactor loop
        if start_reactor:
            reactor.run()


        # if we exited due to a connection error, raise that to the
        # caller
        if connect_error.exception:
            raise connect_error.exception

