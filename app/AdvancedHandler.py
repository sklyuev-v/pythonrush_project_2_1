import json
import os.path

from http.server import BaseHTTPRequestHandler

from loguru import logger
from typing import NoReturn, Literal


from Router import Router
from settings import STATIC_PATH
from settings import ERROR_FILE_404


class AdvancedHTTPRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        self.default_response = lambda: self.send_html(ERROR_FILE_404, 404)
        self.router = Router()
        super().__init__(request, client_address, server)

    def send_html(self, filename: str,
                  code: int = 200,
                  headers: dict = None,
                  file_path: str = STATIC_PATH) -> NoReturn:

        self.send_response(code)
        self.send_header('Content-type', 'text/html')
        if headers:
            for header, value in headers.items():
                self.send_header(header, value)
        self.end_headers()

        with open(os.path.join(file_path, filename), 'rb') as file:
            self.wfile.write(file.read())

    def send_json(self, respone: dict, code: int = 200,
                  headers: dict = None) -> NoReturn:

        self.send_response(code)
        self.send_header('Content-type', 'application/json')
        if headers:
            for header, value in headers.items():
                self.send_header(header, value)
        self.end_headers()
        self.wfile.write(json.dumps(respone).encode('utf-8'))

    def do_GET(self) -> NoReturn:
        self.do_request('GET')

    def do_POST(self) -> NoReturn:
        self.do_request('POST')

    def do_DELETE(self) -> NoReturn:
        self.do_request('DELETE')

    def do_request(self,
                   method: Literal["GET", "POST", "DELETE"],) -> NoReturn:
        logger.info(f'{method} {self.path}')
        handler, kwargs = self.router.resolve(method, self.path)
        if handler:
            handler(self, **kwargs)
        else:
            logger.warning(f'No handler for {method} {self.path}')
            self.default_response()
