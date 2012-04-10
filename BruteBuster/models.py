# BruteBuster by Cyber Security Consulting (www.csc.bg)

"""
BruteBuster DB model.

It makes use of the BB_MAX_FAILURES and BB_BLOCK_INTERVAL values in
settings.py. If these are not present, default values are used.

Blocks are applied against the unique combination of (user,IP). This means that
a bruteforce attacker won't stop the legitimate user from logging in (assuming
they are using different IP addresses).

The easiest way to remove a block is to delete the FailedAttempt record (e.g.
via the admin).
"""

from django.db import models
from datetime import datetime, timedelta
from django.conf import settings

# default values that can be overriden in settings.py
BB_MAX_FAILURES = int(getattr(settings,'BB_MAX_FAILURES', 5))
BB_BLOCK_INTERVAL = int(getattr(settings,'BB_BLOCK_INTERVAL', 3))

class FailedAttempt (models.Model):
    username = models.CharField('Username',max_length=255)
    IP =  models.IPAddressField('IP Address',null=True)
    failures = models.PositiveIntegerField('Failures',default=0)
    timestamp = models.DateTimeField('Last failed attempt',auto_now=True)

    def too_many_failures (self):
        """Check if the minumum number of failures needed for a block
        is reached"""
        return self.failures >= BB_MAX_FAILURES

    def recent_failure (self):
        """Checks if the timestamp one the FailedAttempt object is
                recent enough to result in an increase in failures"""
        return datetime.now() < self.timestamp + timedelta(minutes=BB_BLOCK_INTERVAL)

    def blocked (self):
        """Shortcut function for checking both too_many_failures and recent_failure """
        return self.too_many_failures() and self.recent_failure()
    blocked.boolean = True

    def __unicode__(self):
        return u'%s (%d failures until %s): ' % (self.username,self.failures, self.timestamp)

    class Meta:
        ordering = ['-timestamp']
        unique_together = (("username", "IP"),)
