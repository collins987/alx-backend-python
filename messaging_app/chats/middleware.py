import logging
import time
from datetime import datetime
from collections import defaultdict

from django.http import HttpResponseForbidden

# ---------- 1. Request Logging Middleware ----------
# Logs all incoming requests with user info and path

logger = logging.getLogger(__name__)
handler = logging.FileHandler('requests.log')
formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        logger.info(f"{datetime.now()} - User: {user} - Path: {request.path}")
        return self.get_response(request)


# ---------- 2. Restrict Access By Time Middleware ----------
# Denies access to the app between 9PM and 6AM server time

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour
        if current_hour < 6 or current_hour >= 21:
            return HttpResponseForbidden("Access is only allowed between 6AM and 9PM.")
        return self.get_response(request)


# ---------- 3. Offensive Language Middleware / Rate Limiter ----------
# Blocks users who send more than 5 messages per minute per IP address

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.ip_message_log = defaultdict(list)  # {ip: [timestamps]}

    def __call__(self, request):
        if request.method == "POST":
            ip = self.get_client_ip(request)
            now = time.time()

            # Remove timestamps older than 60 seconds
            self.ip_message_log[ip] = [t for t in self.ip_message_log[ip] if now - t < 60]

            if len(self.ip_message_log[ip]) >= 5:
                return HttpResponseForbidden("Rate limit exceeded: Max 5 messages per minute.")

            self.ip_message_log[ip].append(now)

        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')


# ---------- 4. Role Permission Middleware ----------
# Only allows users with role 'admin' or 'moderator' to access certain views

class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            role = getattr(request.user, 'role', None)  # Customize based on your user model
            if role not in ['admin', 'moderator']:
                return HttpResponseForbidden("403 Forbidden: Insufficient role permissions.")
        else:
            return HttpResponseForbidden("403 Forbidden: Login required.")
        return self.get_response(request)
