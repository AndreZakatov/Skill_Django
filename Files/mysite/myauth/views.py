from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LogoutView, LoginView
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, CreateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied

from .models import UserProfile
from .forms import ProfileForm


class ProfileEditPermission(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        profile_user = self.get_object()
        return user.is_staff or user == profile_user


class AboutMeView(LoginRequiredMixin, TemplateView):
    template_name = "myauth/about-me.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        context["form"] = ProfileForm(instance=profile)
        return context
    
    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        form = ProfileForm(instance=profile, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect("myauth:about-me")
        return self.render_to_response(self.get_context_data(form=form))


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "myauth/register.html"
    success_url = reverse_lazy("myauth:about-me")

    def form_valid(self, form):
        response = super().form_valid(form)
        UserProfile.objects.create(user=self.object)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        user = authenticate(
            self.request,
            username=username,
            password=password,
        )
        login(request=self.request, user=user)
        return response


class MyLogoutView(LogoutView):
    next_page = reverse_lazy("myauth:login")


@user_passes_test(lambda u: u.is_superuser)
def set_cookie_view(request: HttpRequest) -> HttpResponse:
    response = HttpResponse("Cookie set")
    response.set_cookie("fizz", "buzz", max_age=3600)
    return response


def get_cookie_view(request: HttpRequest) -> HttpResponse:
    value = request.COOKIES.get("fizz", "default value")
    return HttpResponse(f"Cookie value: {value!r}")


@permission_required("myauth.view_profile", raise_exception=True)
def set_session_view(request: HttpRequest) -> HttpResponse:
    request.session["foobar"] = "spameggs"
    return HttpResponse("Session set!")


@login_required
def get_session_view(request: HttpRequest) -> HttpResponse:
    value = request.session.get("foobar", "default")
    return HttpResponse(f"Session value: {value!r}")


class FooBarView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        return JsonResponse({"foo": "bar", "spam": "eggs"})


class UserDetailView(LoginRequiredMixin, DetailView):
    template_name = "myauth/user-detail.html"
    model = User
    context_object_name = "user_obj"
    queryset = User.objects.select_related("userprofile")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"User {self.object.username}"
        context["can_edit"] = self.request.user.is_staff or self.request.user == self.object
        return context


class UserListView(LoginRequiredMixin, ListView):
    template_name = "myauth/users-list.html"
    context_object_name = "users"
    queryset = User.objects.select_related("userprofile").all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Users List"
        return context


class UserProfileUpdateView(LoginRequiredMixin, ProfileEditPermission, TemplateView):
    template_name = "myauth/user-profile-update.html"
    model = UserProfile

    def get_object(self):
        user = User.objects.get(pk=self.kwargs["pk"])
        return user.userprofile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        context["form"] = ProfileForm(instance=profile)
        context["user_obj"] = profile.user
        return context

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        profile = self.get_object()
        form = ProfileForm(instance=profile, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect("myauth:user-detail", pk=profile.user.pk)
        return self.render_to_response(self.get_context_data(form=form))

    def render_to_response(self, context):
        return TemplateView.render_to_response(self, context)
