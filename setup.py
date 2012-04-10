#!/usr/bin/env python
#import ez_setup
#ez_setup.use_setuptools()
from setuptools import setup, find_packages

setup(\
    name = "django-brutebuster",
    version = "0.1.8",
    packages = find_packages(),
    author = "Cyber Security Consulting Ltd.",
    author_email = "contact@csc.bg",
    description = "Pluggable Django application providing password bruteforce protection",
    url = "http://code.google.com/p/django-brutebuster/",
    include_package_data = True,
    zip_safe = False
)
