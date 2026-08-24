from django.urls import path

from . import views

urlpatterns = [

    path(
        "",
        views.home,
        name="home",
    ),

    path(
        "login/",
        views.login_admin,
        name="login",
    ),

    path(
        "dashboard/",
        views.dashboard,
        name="dashboard",
    ),

    path(
        "logout/",
        views.sair,
        name="logout",
    ),

    path(
        "recuperar-admin/",
        views.recuperar_admin,
        name="recuperar_admin",
    ),

]