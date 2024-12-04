from django.shortcuts import redirect
from django.urls import reverse_lazy

from django.views.generic import CreateView
from django.views import View

from django.contrib.auth.models import User
from django.contrib.auth import login, logout

from .forms import RegisterForm


class RegisterView(CreateView):
    model = User
    template_name = "accounts/register.html"
    form_class = RegisterForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        valid = super().form_valid(form)
        login(self.request, self.object)
        return valid


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')
