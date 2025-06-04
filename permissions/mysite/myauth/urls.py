from django.urls import path
from django.contrib.auth.views import LoginView
from .views import (LoginView,
                    get_cookie_view,
                    set_cookie_view,
                    get_session_view,
                    set_session_view,
                    MyLogOutView,
                    AboutMeView,
                    RegisterView,
                    )


app_name = "myauth"

urlpatterns = [
    path(
        'login/',
        LoginView.as_view(
            template_name="myauth/login.html",
            redirect_authenticated_user=True,
            ),
        name="login",
        ),
    path("logout/", MyLogOutView.as_view(), name="logout"),
    path("me/", AboutMeView.as_view(), name="about-me" ),
    path("register/", RegisterView.as_view(), name="register"),

    path("cookie/get/", get_cookie_view, name="cookei-get"),
    path("cookie/set/", set_cookie_view, name="cookei-set"),

    path("session/set/", set_session_view, name="session-set"),
    path("session/get/", get_session_view, name="session-get"),
]