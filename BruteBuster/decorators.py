# BruteBuster by Cyber Security Consulting (www.csc.bg)

"""Decorators used by BruteBuster"""

from BruteBuster.models import FailedAttempt
from BruteBuster.middleware import get_request

def protect_and_serve (auth_func):
    """
    This is the main code of the application. It is meant to replace the
    authentication() function, with one that records failed login attempts and
    blocks logins, if a threshold is reached
    """

    if hasattr(auth_func,'__BB_PROTECTED__'):
        # avoiding multiple decorations
        return auth_func
    
    def decor (*args, **kwargs):
        """
        This is the wrapper that gets installed around the default
        authentication function.
        """
        user = kwargs.get('username','')
        if not user:
            raise ValueError ('BruteBuster cannot work with authenticate functions that do not include "username" as an argument')
        
        request = get_request()
        if request:
            # try to get the remote address from thread locals
            IP_ADDR = request.META.get('REMOTE_ADDR',None)
        else:
            IP_ADDR = None
        
        try:
            fa = FailedAttempt.objects.filter(username=user,IP=IP_ADDR)[0]
            if fa.recent_failure():
                if fa.too_many_failures() :
                    # we block the authentication attempt because
                    # of too many recent failures
                    fa.failures += 1
                    fa.save()
                    return None
            else:
                # the block interval is over, so let's start
                # with a clean sheet
                fa.failures = 0
                fa.save()
        except IndexError:
            # No previous failed attempts
            fa = None

        result = auth_func (*args, **kwargs)
        if result:
            # the authentication was successful - we do nothing
            # special
            return result
        # the authentication was kaput, we should record this
        fa = fa or FailedAttempt (username=user,IP=IP_ADDR,failures=0)
        fa.failures+=1
        fa.save()
        # return with unsuccessful auth
        return None

    decor.__BB_PROTECTED__ = True
    return decor
