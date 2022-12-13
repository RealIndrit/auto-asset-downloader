from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading
import time

PORT = 5500
HOST = 'localhost'


class HTTPServerLayer(object):

    def setUp(self):
        self.server = None
        self.host = HOST
        self.port = PORT
        self.start_server()

    def start_server(self):
        self.server = HTTPServer((self.host, self.port),
                                 SimpleHTTPRequestHandler)
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()
        time.sleep(0.25)

    def stop_server(self):
        if self.server is None:
            return
        self.server.shutdown()
        self.server_thread.join()

    def tearDown(self):
        self.stop_server()