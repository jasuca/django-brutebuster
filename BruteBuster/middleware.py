# BruteBuster by Cyber Security Consulting (www.csc.bg)

"""
Brutebuster needs access to the REMOTE_IP of the incoming request. We're doing
this by adding the request object to the thread_local space
"""
import sys

try:
    from threading import local
except ImportError:
    from django.utils._threading_local import local

_thread_locals = local()

def get_request():
    return getattr(_thread_locals, 'request', None)

class RequestMiddleware (object):
    """Provides access to the request object via thread locals"""
    def process_request (self, request):
        _thread_locals.request = request
