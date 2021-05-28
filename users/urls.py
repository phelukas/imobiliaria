from django.conf.urls import url
from . import views


app_name = 'login'

urlpatterns = [
    url(r'^$', views.UserFormView.as_view(), name='loginview'),
    # logout
    url(r'^logout/$', views.UserLogoutView.as_view(), name='logoutview'),
    # login/criarperfil/
    url(r'^criarperfil/$', views.CriarPefilView.as_view(), name='criarperfilview'),
]

