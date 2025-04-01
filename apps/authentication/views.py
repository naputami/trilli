from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.views import View
from .forms import UserRegistrationForm, LoginForm

from core.views import LoginRequiredViewMixin


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
            print(form.errors)
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
                return redirect("board")  # Replace with your home page URL name
            else:
                messages.error(request, "Invalid username or password")
                return render(request, "login.html", {"form": form})
        else:
            return render(request, "login.html", {"form": form})


class LogoutView(LoginRequiredViewMixin, View):
    def post(self, request):
        print("logout")
        logout(request)
        return redirect("login")
