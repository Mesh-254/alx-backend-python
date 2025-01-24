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
        start_time = datetime.strptime('18:00:00', '%H:%M:%S').time()
        end_time = datetime.strptime('21:00:00', '%H:%M:%S').time()
        if current_time < start_time or current_time > end_time:
            return HttpResponse(
                "<div style='text-align: center; font-weight: bold; color: red; font-size: 20px; margin:200px auto;'>"
                f"Sorry, the service is only available from {
                    start_time} to {end_time}</div>",
                status=403,
                content_type='text/html'
            )

        response = self.get_response(request)

        return response


class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        messsage_limit = 5
        time_limit = 5 * 60  # 5 minutes in seconds

        # Get the user's IP address
        ip_address = request.META.get(
            'HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR'))

       # session storage to maintain message history per IP
        if 'message_history' not in request.session:
            request.session['message_history'] = {}

        message_history = request.session['message_history']

        # Get the current timestamp
        current_time = now().timestamp()

        # Initialize IP's message history if not present
        if ip_address not in message_history:
            message_history[ip_address] = []

        # Check if the user has sent too many messages
        if request.method == 'POST' and len(message_history[ip_address]) >= messsage_limit:
            return HttpResponse(
                "<div style='text-align: center; font-weight: bold; color: red; font-size: 20px; margin:200px auto;'>"
                "Message limit exceeded. Please wait a few minutes before trying again.</div>",
                status=429,
                content_type='text/html'
            )

        # add new message to the history
        if request.method == 'POST':
            message_history[ip_address].append(current_time)
            request.session['message_history'] = message_history

        # Proceed with the original response
        response = self.get_response(request)

        return response

class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        
        # Check if the user is authenticated
        if request.user.is_authenticated:
            # Allow access for admin users
            if request.user.role == 'admin':
                return self.get_response(request)
                
            # Restrict access for non-admin users
            else:
                return HttpResponse(
                    "<div style='text-align: center; font-weight: bold; color: red; font-size: 20px; margin:200px auto;'>"
                    "Restricted: You don't have permission to access this page.</div>",
                    status=403,
                    content_type='text/html'
                )

        # For unauthenticated users, allow request to proceed (if needed)
        return self.get_response(request)
