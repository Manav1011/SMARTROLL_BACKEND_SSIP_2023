"""
URL configuration for SMARTROLL project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include,re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from .views import check_server_avaibility,check_token_authenticity,handle404,TeacherActivation,ForgotPasswordPage
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve


schema_view = get_schema_view(
    openapi.Info(
        title="Your API",
        default_version='v1',
        description="Your API description",
        terms_of_service="https://www.yourapp.com/terms/",
        contact=openapi.Contact(email="contact@yourapp.com"),
        license=openapi.License(name="Your License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # path('', TemplateView.as_view(template_name='index.html'), name='home'),
    # path('__debug__/', include('debug_toolbar.urls')),
    path('teacher_activation/<str:slug>',TeacherActivation),
    path('forgot_password/<str:slug>',ForgotPasswordPage),
    path('',TemplateView.as_view(template_name='index.html')),
    path('scatter',TemplateView.as_view(template_name='scatter.html')),
    path('smartroll@admin.private/', admin.site.urls),
    path('check_server_avaibility/', check_server_avaibility,name='check_server_avaibility'),
    path('check_token_authenticity/', check_token_authenticity,name='check_token_authenticity'),
    path('auth/',include('StakeHolders.urls')),
    path('manage/',include('Manage.urls')),        
    re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
    re_path(r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT}),    
    # path('api_endpoints/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

handler404 = 'SMARTROLL.views.handle404'