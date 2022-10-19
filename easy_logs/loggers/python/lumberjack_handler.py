import time
import logging
import socket
import signal
import ssl
try:
    import ujson as json
except ImportError:
    import json
from multiprocessing import Process, Event
from json.decoder import JSONDecodeError
from struct import pack, unpack
import zlib

from easy_logs.loggers.python.models import insert_python_lumberjack_handler


logging.basicConfig()

logger = logging.getLogger('easylogs')
logger.setLevel(logging.DEBUG)


class LumberjackReceiver:
    def __init__(self):
        self.running = True

    def signal_handler(self, sig, frame):
        self.running = False

    def _recv(self, conn, size):
        data = b''
        while len(data) != size:
            try:
                ndata = conn.recv(size - len(data))
            except BlockingIOError:
                if not self.running:
                    raise Exception("STOP WORKERS SIGNAL")
                time.sleep(1)
                continue

            if not len(ndata):
                raise Exception('[recv] Connection closed')
            data += ndata
        return data

    def recv_full_msg(self, conn):
        """frame window size - 6 bytes
        B - version
        B - type frame
        I - window size

        frame json - 10 bytes
        B - version
        B - type frame
        I - Sequence (ack id)
        I - Json length

        frame compressed - 6 bytes
        B - version
        B - type frame
        I - compressed size
        When decompressing the data contains a normal structure,
        it will have a json frame and will contain several concatenated json

        frame ack - 6 bytes
        B - version
        B - type frame
        I - Sequence (ack id)
        """
        buffer = b''
        while self.running:
            raw = self._recv(conn, 2)
            base = unpack('>BB', raw)
            if base[1] == 0x57:
                # start message
                self._recv(conn, 4)
                continue

            elif base[1] == 0x43:
                # compress
                jsonsize = unpack('>I', self._recv(conn, 4))[0]
                buffer += zlib.decompress(self._recv(conn, jsonsize))

            elif base[1] == 0x4A:
                # json
                info = self._recv(conn, 8)
                buffer += raw + info
                sequence, jsonsize = unpack('>II', info)
                buffer += self._recv(conn, jsonsize)
            else:
                break

            while buffer:
                base = unpack('>BB', buffer[:2])
                if base[1] == 0x4A:
                    # json
                    l = 10
                    version, _, sequence, jsize = unpack('>BBII', buffer[:l])
                else:
                    break

                result = buffer[l:jsize+l]
                if version != 0x00:
                    conn.send(pack('>BBI', version, 65, sequence))
                yield result
                buffer = buffer[jsize+l:]
        raise StopIteration("stop ongoing")

    def reader(self, conn):
        messages = self.recv_full_msg(conn)
        while self.running:
            try:
                insert_python_lumberjack_handler(
                    **self.parse_data(next(messages))
                )
            except Exception as ex:
                logger.error(ex)
                break
        conn.close()
        print('[reader] Stopped')

    def parse_data(self, data):
        try:
            info = json.loads(data)
            return {
                "log_name": info['log']['file']['path'],
                "message": info['message']
            }

        except Exception:
            raise JSONDecodeError

    def run(self):
        signal.signal(signal.SIGINT, self.signal_handler)
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # TODO: SSL implementation

        # context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        # context.load_cert_chain(certfile='/tmp/MyCertificate.crt', keyfile='/tmp/MyKey.key')
        # sock = context.wrap_socket(
        #     sock=sock,
        #     server_side=True)

        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Bind the socket to the port
        server_address = ('0.0.0.0', 5044)
        logger.info('starting up on {} port {}'.format(*server_address))
        sock.bind(server_address)
        sock.setblocking(False)

        # Listen for incoming connections
        sock.listen(128)

        logger.info('Waiting for a connection')
        while self.running:
            try:
                connection, client_address = sock.accept()
                connection.setblocking(False)
            except BlockingIOError:
                time.sleep(1)
                continue
            except ssl.SSLError as ex:
                print(ex)
                continue
            logger.info('Connection from %s', client_address)
            Process(target=self.reader, args=(connection,)).start()

        sock.close()
        logger.info('Socket closed')


if __name__ == '__main__':
    LumberjackReceiver().run()