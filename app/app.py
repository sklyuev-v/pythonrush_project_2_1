from http.server import HTTPServer, BaseHTTPRequestHandler
from http.server import SimpleHTTPRequestHandler
from PIL import Image
from loguru import logger
import io
from os import listdir
from os.path import isfile, join
import multipart as mp
import hashlib
import json


VALID_FILE_FORMATS = ('JPEG', 'GIF', 'PNG')
SERVER_ADRESS = ('0.0.0.0', 8000)

logger.add('logs/app.log',
           format="[{time: YYYY-MM-DD HH:mm:ss}] | {level} | {message}")


class ImageHostingHandler(BaseHTTPRequestHandler):
    server_version = 'Image Hosting Server/0.2'

    def __init__(self, request, client_adress, server):
        """Defines allowed routes for GET and POST requests"""
        self.get_routes = {
            '/upload': ImageHostingHandler.get_upload,
            '/images': ImageHostingHandler.get_images,
        }

        self.post_routes = {
            '/upload': ImageHostingHandler.post_upload,
        }

        super().__init__(request, client_adress, server)

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        SimpleHTTPRequestHandler.end_headers(self)

    def do_GET(self):
        """GET requests handler
        """
        if self.path in self.get_routes:
            self.get_routes[self.path](self)
        else:
            logger.warning(f'GET 404 {self.path}')
            self.send_response(404, 'Not Found')

    def get_images(self):
        """Gets list of images from images/ directory,
        for js script on images webpage.
        """
        logger.info(f'GET {self.path}')
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.end_headers()

        images = [f for f in listdir(
            './images') if isfile(join('./images', f))]
        self.wfile.write(json.dumps({'images': images}).encode('utf-8'))

    def get_upload(self):
        """Simple load upload.html by GET request
        """
        logger.info(f'GET {self.path}')
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(open('static/upload.html', 'rb').read())

    def do_POST(self):
        """POST requests handler
        """
        if self.path in self.post_routes:
            self.post_routes[self.path](self)
        else:
            logger.warning(f'POST 404 {self.path}')
            self.send_response(405, 'Method Not Allowed')

    def post_upload(self):
        """
        Work on POST request.
        Gets file body from multipart/form-data with multipart,
        check file type with Pillow,
        save image in images/ directory,
        redirect user to image success download page.
        """
        logger.info(f'POST {self.path}')
        content_type = self.headers['Content-Type']

        if 'multipart/form-data' in content_type:
            content_length = int(self.headers['Content-Length'])

            webkit_boundary = content_type.split(' ')[1].split('=')[1]

            post_data = self.rfile.read(content_length)

            p = mp.MultipartParser(io.BytesIO(post_data), webkit_boundary)
            parts = p.parts()
            image_raw_data = io.BytesIO(parts[0].raw)
            image_ext = parts[0].filename.split('.')[1]

            filename = hashlib.file_digest(
                image_raw_data, 'md5').hexdigest()

            try:
                with Image.open(image_raw_data) as img:
                    logger.error(img.format)
                    if img.format in VALID_FILE_FORMATS:
                        img.save(f'images/{filename}.{image_ext}')
                    else:
                        logger.error('File type is not allowed')
                        self.send_response(400, 'File type not allowed')
                        return
            except Exception as e:
                self.send_response(400, 'File type not allowed')
                logger.error(e)
                return

            logger.info(f'Upload success: {filename}.{image_ext}')

            with open('static/upload_success.html', 'r') as f:
                upload_suc_page = f.read()

            html_page = upload_suc_page.replace(
                '{image_filename}', f'{filename}.{image_ext}')

            self.send_response(301)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()

            self.wfile.write(bytes(html_page, "utf8"))


def run_server(server_class=HTTPServer, handler_class=ImageHostingHandler):
    """This function runs HTTP Server.
    You can stop the server by press Ctrl+C
    """
    httpd = server_class(SERVER_ADRESS, handler_class)
    try:
        logger.info(f'Serving at http://{SERVER_ADRESS[0]}:{SERVER_ADRESS[1]}')
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.info('Server stopped by Keyboard Interrupt')
        httpd.server_close()


if __name__ == '__main__':
    run_server()
