from django.utils.timezone import now  # Use Django's timezone-aware datetime
import logging
from datetime import datetime

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        # One-time configuration and initialization.
        self.get_response = get_response

        # Configure the logger (only once)
        logging.basicConfig(
            filename='requests.log',
            level=logging.INFO,
            format='%(asctime)s - User: %(message)s - Path: %(pathname)s',
        )
        self.logger = logging.getLogger('request_logger')

    def __call__(self, request):
        # Logging info before the view is called
        user = request.user.username if request.user.is_authenticated else "Anonymous"
        logging.info(f"{datetime.now()} - User: {user} - Path: {request.path}")

        # Process the response
        response = self.get_response(request)

        return response
