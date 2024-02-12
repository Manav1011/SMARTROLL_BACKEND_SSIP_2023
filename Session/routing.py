from django.urls import re_path
from .consumers import AttendanceSessionConsumer

attendance_session_urlpatterns = [
    re_path(r"ws/attendance_session/(?P<session_id>\w+)/$", AttendanceSessionConsumer.as_asgi()),
]
