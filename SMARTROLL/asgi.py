"""
ASGI config for SMARTROLL project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SMARTROLL.settings')
import django
django.setup()
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter,URLRouter
from Session.routing import attendance_session_urlpatterns
import netifaces as ni
interface = ni.gateways()['default'][ni.AF_INET][1]
local_ip = ni.ifaddresses(interface)[ni.AF_INET][0]['addr']
os.environ['router_network_addr'] = '.'.join(local_ip.split('.')[:2])
application = get_asgi_application()

application = ProtocolTypeRouter({
    "http": application,
    "websocket": URLRouter(attendance_session_urlpatterns)
})
