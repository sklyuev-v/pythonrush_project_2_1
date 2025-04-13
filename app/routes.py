from Router import Router
from AdvancedHandler import AdvancedHTTPRequestHandler


def register_routes(router: Router, handler_class: AdvancedHTTPRequestHandler):
    router.add_route('GET', '/api/images/', handler_class.get_images)
    router.add_route('POST', '/upload/', handler_class.post_upload)
