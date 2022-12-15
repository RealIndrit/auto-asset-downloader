from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading
import time


class HTTPServerLayer:

    def __init__(self, host="localhost", port=5500):
        self.host = host
        self.port = port
        self.server = None

    def setUp(self):
        self.__start_server()
        print(f"Local Http Server on {self.host}:{self.port} has been started")

    def __start_server(self):
        self.server = HTTPServer((self.host, self.port),
                                 SimpleHTTPRequestHandler)
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()
        time.sleep(0.25)

    def __stop_server(self):
        if self.server is None:
            return
        self.server.shutdown()
        self.server_thread.join()

    def tearDown(self):
        self.__stop_server()
        print(
            f"Local Http Server on {self.host}:{self.port} has been shutdown")
