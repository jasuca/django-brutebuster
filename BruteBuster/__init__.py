# BruteBuster by Cyber Security Consulting (www.csc.bg)
"""
Module preventing Brute Force attacks against
django.contrib.auth.authenticate()
"""

version = '0.1.8'

from django.contrib import auth
from BruteBuster.decorators import protect_and_serve

# here we override the default authenticate method with the decorated version
auth.authenticate  = protect_and_serve (auth.authenticate)
