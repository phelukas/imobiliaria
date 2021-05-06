from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView, FormView, ListView, DeleteView
from django.contrib.auth import login, logout, get_user_model

from .form import UserLoginForm

# Create your views here.
class UserFormView(View):
    form_class = UserLoginForm
    template_name = 'account/login.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST or None)
        if request.POST and form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = form.authenticate_user(username=username, password=password)
            if user:
                login(request, user)
                return redirect('base:index')

        return render(request, self.template_name, {'form': form})
