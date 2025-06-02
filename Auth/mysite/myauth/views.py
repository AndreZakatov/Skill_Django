from django.contrib.auth.views import LogoutView, LoginView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy


# def login_view(request):
#     if request.method == "GET":
#         if request.user.is_authenticated:
#             print("Redirecting to products list")
#             return redirect(reverse_lazy("shopapp:products_list"))
#         return render(request, 'myauth/login.html')
#
#     username = request.POST.get('username')
#     password = request.POST.get('password')
#
#     user = authenticate(request, username=username, password=password)
#     if user is not None:
#         login(request, user)
#         print("Redirecting to products list after login")
#         return redirect(reverse_lazy("shopapp:products_list"))
#     return render(request, "myauth/login.html", {"error": "Error login credential"})


class LoginView(LoginView):
    template_name = "myauth/login.html"
    redirect_authenticated_user = True
    success_url = reverse_lazy("shopapp:products_list")



class MyLogOutView(LogoutView):
    next_page = reverse_lazy("myauth:login")

def set_cookie_view(request: HttpRequest) -> HttpResponse:
    response = HttpResponse("Cookie set")
    response.set_cookie(
        key="fizz",
        value="buzz",
        max_age=3600,
        httponly=True,
        secure=True,
        )
    return response

def get_cookie_view(request: HttpRequest) -> HttpResponse:
    value = request.COOKIES.get("fizz", "default value")
    return HttpResponse(f"Cookie value: {value!r}")


def set_session_view(request: HttpRequest) -> HttpResponse:
    request.session["foobar"] = "spameggs"
    return HttpResponse("session set!")


def get_session_view(request: HttpRequest) -> HttpResponse:
    value = request.session.get("foobar", "default")
    return HttpResponse(f"Session value: {value!r}")