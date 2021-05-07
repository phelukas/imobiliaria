from django.conf.urls import url
from . import views 

app_name = 'core'

urlpatterns = [

    # LISTA DE IMOVEIS
    url(r'^home/$', views.Index.as_view(), name='index'),

    # CRUD CLIENTE
    url(r'clientes/$', views.ListarClienteView.as_view(), name='listacliente'),
    url(r'addcliente/$', views.AdicionaClienteView.as_view(), name='addcliente'),
    url(r'editcliente/(?P<pk>[0-9]+)/$', views.EditarClienteView.as_view(), name='editcliente'),
    url(r'deletarliente/(?P<pk>[0-9]+)/$', views.DeletarClienteView.as_view(), name='delcliente'),

    # VENDA
    url(r'imovel/(?P<pk>[0-9]+)/$', views.AdicionarVendaView.as_view(), name='addvenda'),
    url(r'listaclientevenda/$', views.ListaClienteVendaView.as_view(), name='listaclientevenda')
]
