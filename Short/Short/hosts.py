from django.conf import settings
from django_hosts import patterns, host

from Short.hostsconf import urls

host_patterns = patterns('',
    host(r'www', settings.ROOT_URLCONF, name='www'),
    host(r'(?!www).*', urls, name='wildcard'),
)