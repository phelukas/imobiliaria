from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import login, logout
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from .form import UserLoginForm, CriarUserForm


class UserFormView(View):
    form_class = UserLoginForm
    template_name = 'account/login.html'

    def get(self, request):
        form = self.form_class(None)

        if request.user.is_authenticated:
            return redirect('core:index')
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST or None)
        if request.POST and form.is_valid():
            username = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = form.authenticate_user(username=username, password=password)
            if user:
                login(request, user)
                return redirect('core:index')
        return render(request, self.template_name, {'form': form})


class CriarPefilView(CreateView):

    form_class = CriarUserForm
    template_name = 'account/criar_perfil.html'
    success_url = reverse_lazy('login:loginview')

    def get(self, request, *args, **kwargs):
        return super(CriarPefilView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        print('aqui')
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            self.object = form.save(commit=False)
            self.object.save()            
            return self.form_valid(form)
        return self.form_invalid(form=form)

class UserLogoutView(View):

    def get(self, request):
        logout(request)
        return redirect("login:loginview")
