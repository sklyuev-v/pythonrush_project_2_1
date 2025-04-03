import os
from http.server import HTTPServer

from loguru import logger

from ImageHostingHandler import ImageHostingHandler
from Router import Router
from routes import register_routes

from settings import SERVER_ADDRESS
from settings import LOG_PATH, LOG_FILENAME_APP
from settings import LOG_MESSAGE_FORMAT


def run_server(server_class=HTTPServer, handler_class=ImageHostingHandler):
    """This function runs HTTP Server.
    You can stop the server by press Ctrl+C
    """
    logger.add(os.path.join(LOG_PATH, LOG_FILENAME_APP),
               format=LOG_MESSAGE_FORMAT)

    router = Router()
    register_routes(router, handler_class)

    httpd = server_class(SERVER_ADDRESS, handler_class)

    try:
        logger.info(
            f'Serving at http://{SERVER_ADDRESS[0]}:{SERVER_ADDRESS[1]}')
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.warning('Keyboard interrupt received, stopping server.')
        httpd.server_close()
    finally:
        logger.info('Server stopped.')


if __name__ == '__main__':
    run_server()
