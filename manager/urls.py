"""Specify URLs for manager"""


from django.urls import path

from manager import views

urlpatterns = [
    path(
        "attribute-cateogries/",
        views.AttributeCategoryListView.as_view(),
        name="attribute-categories",
    ),
    path("register/", views.UserRegisterView.as_view(), name="register"),
]
