from django.contrib import admin
from django.urls import include, path

from rest_framework import routers

from core import views as core_views

api_router = routers.DefaultRouter(trailing_slash=False)
api_router.register(r"schools", core_views.SchoolViewSet)
api_router.register(r"courses", core_views.CourseViewSet)
api_router.register(r"admins", core_views.AdministratorViewSet)
api_router.register(r"teachers", core_views.TeacherViewSet)
api_router.register(r"students", core_views.StudentViewSet)


urlpatterns =  [
    path('admin/', admin.site.urls),
    path('api/', include(api_router.urls)),
    path('api/transfer', core_views.TransferView.as_view(), name='transfer')
]