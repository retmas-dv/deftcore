__author__ = 'Dmitry Golubkov'

import ssl
import stomp
from deftcore.settings import VOMS_CERT_FILE_PATH, VOMS_KEY_FILE_PATH, MessagingConfig
from .listener import Listener


class Client(object):
    _id = 0

    def __init__(self, hostname, port, logger, no_db_log=False):
        self._logger = logger
        self.id = Client._id
        Client._id += 1

        cert_file = VOMS_CERT_FILE_PATH
        key_file = VOMS_KEY_FILE_PATH

        self.connection = stomp.Connection(
            host_and_ports=[(hostname, port)],
            use_ssl=True, ssl_version=ssl.PROTOCOL_TLSv1,
            ssl_key_file=key_file,
            ssl_cert_file=cert_file,
            keepalive=True,
            heartbeats=(10000, 10000)
        )

        self.connection.set_listener('messaging_listener', Listener(self, logger, no_db_log=no_db_log))

    def connect(self):
        try:
            if self.is_connected():
                self.disconnect()

            self.connection.start()
            self.connection.connect(wait=True)
            self.connection.subscribe(destination=MessagingConfig.QUEUE, id=str(self.id), ack='auto')
            self._logger.info('id={0}'.format(self.id))
        except Exception as ex:
            self._logger.error('exception occurred: {0}'.format(str(ex)))

    def disconnect(self):
        self.connection.disconnect()

    def is_connected(self):
        return self.connection.is_connected()
