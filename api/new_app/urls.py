from django.contrib import admin
from django.urls import include, path

from rest_framework import routers

from core import views as core_views

api_router = routers.DefaultRouter(trailing_slash=False)
api_router.register(r"schools", core_views.SchoolViewSet)


urlpatterns =  [
    path('admin/', admin.site.urls),
    path('api/', include(api_router.urls)),
]