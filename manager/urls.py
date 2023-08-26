"""Specify URLs for manager."""


from django.urls import path

from manager import views


urlpatterns = [
    path(
        "attribute-cateogries/",
        views.AttributeCategoryListView.as_view(),
        name="attribute-categories",
    ),
    path("register/", views.UserRegisterView.as_view(), name="register"),
    path("managers/", views.ManagerListView.as_view(), name="manager-list"),
    path("countries/", views.CountryListView.as_view(), name="countries"),
    path("leagues/", views.LeagueListView.as_view(), name="league-list"),
    path("teams/", views.TeamListView.as_view(), name="team-list"),
]
