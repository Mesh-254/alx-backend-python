from django.utils.timezone import now  # Use Django's timezone-aware datetime
import logging
from datetime import datetime
from django.http import HttpResponse


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


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_time = now().time()
        if current_time < datetime.strptime('08:00:00', '%H:%M:%S').time() or current_time > datetime.strptime('11:00:00', '%H:%M:%S').time():
            return HttpResponse(
                "<div style='text-align: center; font-weight: bold; color: red; font-size: 20px; margin:200px auto;'>"
                "Sorry, the service is only available from 08:00 to 17:00.</div>",
                status=403,
                content_type='text/html'
            )

        response = self.get_response(request)

        return response
    


