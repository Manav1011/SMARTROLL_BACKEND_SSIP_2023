from django.urls import path
from .views import add_event,get_events,end_event,upload_results,notify_users_about_emergency

urlpatterns = [
    path('add_event/',add_event,name='add_event'),
    path('get_events',get_events,name='get_events'),
    path('end_event',end_event,name='end_event'),
    path('upload_results/',upload_results,name='upload_results'),
    path('notify_users_about_emergency/',notify_users_about_emergency,name='notify_users_about_emergency'),
]
