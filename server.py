import socketserver
from datetime import datetime, timedelta
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import json
from typing import Tuple
from parser import get_exchange_rates


def current_moscow_time():
    return (
        datetime.combine(datetime.now().date(), datetime.min.time())
        + timedelta(hours=3)
    )

UPDATE_PERIOD = 1


class Server(BaseHTTPRequestHandler):

    def __init__(
            self, request: bytes, client_address: Tuple[str, int],
            server: socketserver.BaseServer
    ):
        self.rates = get_exchange_rates()
        self._set_next_update_time()
        super().__init__(request, client_address, server)

    def _check_update_time(self):
        time = current_moscow_time()
        if time <= self._next_update_time:
            logging.info('Updating exchange rates...')
            self.rates = get_exchange_rates()
            self._set_next_update_time()

    def _set_next_update_time(self):
        time = current_moscow_time()
        self._next_update_time = time + timedelta(hours=UPDATE_PERIOD)

    def _set_response(self, code: int = 200, response: dict = None) -> None:
        if not response:
            response = dict()
        response = json.dumps(response).encode()
        self.send_response(code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(response)

    def do_GET(self) -> None:
        logging.info(
            f"{str(self.command)} request,\nPath: {str(self.path)}\nHeaders:"
            f"\n{str(self.headers)}\n"
        )
        if self.path == '/':
            self._check_update_time()
            code = 200
            if self.rates.get('error'):
                code = 400
            self._set_response(code, self.rates)
            self.log_error(str(self.rates))
        else:
            response = {
                "code": 404, "error": "route not found. Proceed to <service>/"
            }
            self._set_response(404, response)
            self.log_error(str(response))


def run(server_class=HTTPServer, handler_class=Server, host='', port=8080):
    logging.basicConfig(level=logging.INFO)
    server_address = (host, port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')
