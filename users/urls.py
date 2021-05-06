from django.conf.urls import url
from . import views


app_name = 'login'

urlpatterns = [
    url(r'^$', views.UserFormView.as_view(), name='loginview')
]

