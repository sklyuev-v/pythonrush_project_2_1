from PIL import Image
from loguru import logger
import io
import os
import hashlib
from urllib.parse import parse_qs
from typing import NoReturn

from settings import VALID_FILE_FORMATS
from settings import SERVER_VERSION
from settings import IMAGES_PATH
from settings import ERROR_FILE_404

from AdvancedHandler import AdvancedHTTPRequestHandler
from DBManager import DBManager


class ImageHostingHandler(AdvancedHTTPRequestHandler):
    server_version = SERVER_VERSION

    def __init__(self, request, client_adress, server):
        self.db = DBManager()
        super().__init__(request, client_adress, server)

    def get_images(self, limit: int) -> NoReturn:
        """Gets list of images from database,
        for js script on images webpage.

        limit - images count
        """
        logger.info(self.headers.get('Query-String'))
        query_components = parse_qs(self.headers.get('Query-String'))
        page = int(query_components.get('page', ['1'])[0])

        if page < 1:
            page = 1

        images = self.db.get_images(page, limit)

        images_json = []

        for image in images:
            image = {
                'filename': image[1],
                'original_name': image[2],
                'size': image[3],
                'upload_date': image[4].strftime('%Y-%m-%d %H:%M:%S'),
                'file_type': image[5]
            }
            images_json.append(image)

        self.send_json({'images': images_json})

    def get_image_gallery(self) -> NoReturn:
        """Gets list of images from database
        for images.html web-page
        """
        self.get_images(limit=9)

    def get_image_list(self) -> NoReturn:
        """Gets list of images from database
        for images-list.html web-page
        """
        self.get_images(limit=10)

    def post_upload(self) -> NoReturn:
        """
        Work on POST request.
        Gets file body from fetch-request on upload page,
        check file type with Pillow,
        save image in database.
        """
        content_length = int(self.headers.get('Content-Length'))

        original_filename, ext = os.path.splitext(self.headers.get('Filename'))
        filedata = self.rfile.read(content_length)
        image_raw_data = io.BytesIO(filedata)

        filename = hashlib.file_digest(image_raw_data, 'md5').hexdigest()
        file_size_kb = round(content_length / 1024)

        self.db.add_image(filename, original_filename, file_size_kb, ext)

        try:
            with Image.open(image_raw_data) as img:
                if img.format in VALID_FILE_FORMATS:
                    img.save(f'{IMAGES_PATH}{filename}{ext}')
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

    def delete_image(self, image_id: str) -> None:
        """This function delete image file
        from hard drive and database

        Args:
            image_id (str): image filename
        """
        logger.info(f'Try to delete image {image_id}')
        filename, ext = os.path.splitext(image_id)
        if not filename:
            logger.warning('Filename header not found')
            self.send_html(ERROR_FILE_404, 404)
            return
        self.db.delete_image(filename)
        image_fullpath = os.path.join(IMAGES_PATH, f'{filename}{ext}')
        if not os.path.exists(image_fullpath):
            logger.warning('Image not found')
            self.send_html(ERROR_FILE_404, 404)
        os.remove(image_fullpath)
        self.send_json({'Success': 'Image deleted'})
