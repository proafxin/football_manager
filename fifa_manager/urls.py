"""fifa_manager URL Configuration.
"""

from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions


title = "Football Manager Fantasy API"
schema_view = get_schema_view(
    openapi.Info(
        title=title,
        default_version="v1",
        description="",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="billalmasum93@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
    path("", include("manager.urls")),
    path("api-auth/", include("rest_framework.urls", namespace="drf")),
    path("api/api-auth/", include("rest_framework.urls")),
    re_path(
        r"^api(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^api/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(
        r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
]
