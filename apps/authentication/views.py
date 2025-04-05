from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.views import View

from core.views import LoginRequiredViewMixin

from .forms import LoginForm, UserRegistrationForm


class RegisterView(View):
    def get(self, request):
        form = UserRegistrationForm()
        return render(request, "register.html", {"form": form})

    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
        else:
            return render(request, "register.html", {"form": form})


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, "login.html", {"form": form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("board")
            else:
                messages.error(request, "Invalid username or password")
                return render(request, "login.html", {"form": form})
        else:
            return render(request, "login.html", {"form": form})


class LogoutView(LoginRequiredViewMixin, View):
    def post(self, request):
        logout(request)
        return redirect("login")
