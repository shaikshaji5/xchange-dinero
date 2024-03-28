# registration/urls.py
from django.urls import path
from . import views

# from .views import register

# app_name = "money"

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="login"),
    path("home/", views.Homepage, name="home"),
    # path("confirm/", views.confirm, name="confirm"),
    path("create_query/", views.create_query, name="create_query"),
    path("add_query/", views.add_query, name="add_query"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("detail/<int:id>/", views.detail, name="detail"),
    path("edit/<int:id>/", views.edit_query, name="edit_query"),
    path("delete/<int:id>/", views.delete_query, name="delete_query"),
]
