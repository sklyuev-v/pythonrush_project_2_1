from PIL import Image
from loguru import logger
import io
import hashlib

from settings import VALID_FILE_FORMATS
from settings import SERVER_VERSION
from settings import IMAGES_PATH

import os

from AdvancedHandler import AdvancedHTTPRequestHandler

from typing import NoReturn


class ImageHostingHandler(AdvancedHTTPRequestHandler):
    server_version = SERVER_VERSION

    def __init__(self, request, client_adress, server):
        super().__init__(request, client_adress, server)

    def get_images(self) -> NoReturn:
        """Gets list of images from images/ directory,
        for js script on images webpage.
        """
        self.send_json({'images': next(os.walk(IMAGES_PATH))[2]})

    def post_upload(self) -> NoReturn:
        """
        Work on POST request.
        Gets file body from fetch-request on upload page,
        check file type with Pillow,
        save image in images/ directory.
        """
        content_length = int(self.headers.get('Content-Length'))
        _, ext = os.path.splitext(self.headers.get('Filename'))
        filedata = self.rfile.read(content_length)
        image_raw_data = io.BytesIO(filedata)

        filename = hashlib.file_digest(image_raw_data, 'md5').hexdigest()

        try:
            with Image.open(image_raw_data) as img:
                if img.format in VALID_FILE_FORMATS:
                    img.save(f'images/{filename}{ext}')
                else:
                    logger.error(
                        f'This image type - {img.format} is not allowed')
                    self.send_response(400, 'File type not allowed')
                    return
        except Exception as e:
            self.send_response(400, 'File type not allowed')
            logger.error(e)
            return

        self.send_response(200)
        self.send_header('Location', f'http://localhost/{IMAGES_PATH}')
        self.send_header('Filename', f'{filename}{ext}')
        self.end_headers()

        logger.info(f'Upload success: {filename}{ext}')
