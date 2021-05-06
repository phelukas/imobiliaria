from django.conf.urls import url
from . import views

app_name = 'core'

urlpatterns = [
    url(r'^home/$', views.Index.as_view(), name='index')
]

