from users.models import User
from django.views.generic import DeleteView, CreateView, ListView, UpdateView
from decimal import Decimal
from django.shortcuts import redirect

from django.urls import reverse_lazy
from django.urls import reverse

from core.models import Imovel, Venda, Cliente, venda
from core.forms import VendaForm, ClienteForm

from django.http import HttpResponse, response


class ListaClienteVendaView(ListView):

    template_name = "venda/lista_venda.html"
    context_object_name = 'all_clientes'

    def get_context_data(self, **kwargs):
        context = super(ListaClienteVendaView, self).get_context_data(**kwargs)
        context['add_url'] = reverse_lazy('core:addvenda')
        context['x'] = Venda.objects.filter(vendedor_user=self.request.user).filter(venda_status=True)
        context['y'] = self.get_queryset().filter(venda_status=True)
        return context        

    def get_queryset(self, **kwrgs):
        f = self.request.GET.get()
        queryset = Venda.objects.filter(vendedor_user=self.request.user)
        return queryset


class AdicionarVendaView(CreateView):

    template_name = "venda/criar_venda.html"
    model = Venda

    def get_success_url(self):
        success_url = reverse('core:checkout', kwargs={
            'pk': self.object.pk,
        })
        return success_url

    def get(self, request, *args, **kwargs):
        self.object = None

        venda_form = VendaForm(prefix='venda_form')

        return self.render_to_response(self.get_context_data(form=venda_form))

    def post(self, request, *args, **kwargs):
        self.object = None

        venda_form = VendaForm(
            request.POST, request.FILES, prefix='venda_form', request=request)

        if venda_form.is_valid():
            self.object = venda_form.save(commit=False)
            self.object.save()
            return self.form_valid(venda_form)

        return self.form_invalid(form=venda_form)


class CheckoutView(UpdateView):

    template_name = 'venda/checkout_venda.html'
    context_object_name = 'all_vendas'

    def get_object(self, queryset=None):
        pk = self.kwargs.get(self.pk_url_kwarg)
        obj = Venda.objects.select_related("cliente_cliente").select_related(
            "imovel_imovel").select_related("vendedor_user").get(pk=pk)
        return obj

    def get_context_data(self, **kwargs):
        context = super(CheckoutView, self).get_context_data(**kwargs)
        context['valor_dividido'] = round(
            (self.object.imovel_imovel.valor/180), 2)
        context['comissao'] = round(
            ((self.object.imovel_imovel.valor) * Decimal(0.05)), 2)
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        venda_form = VendaForm(instance=self.object, prefix='venda_form')

        return self.render_to_response(self.get_context_data(form=venda_form))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        obj = self.object

        print(obj.cliente_cliente.quantidade_compras)

        if obj.venda_status == False:

            obj.venda_status = True
            obj.save()

            obj.imovel_imovel.vendido_status = True
            obj.imovel_imovel.propretario = obj.cliente_cliente
            obj.imovel_imovel.save()

            obj.cliente_cliente.quantidade_compras = obj.cliente_cliente.quantidade_compras + 1
            obj.cliente_cliente.save()

            obj.vendedor_user.quantidade_vendas = obj.vendedor_user.quantidade_vendas + 1
            obj.vendedor_user.save()

        return redirect('core:listavenda')


class DeletarVendaView(DeleteView):

    template_name = 'venda/venda_confirm_delete.html'
    model = Venda
    success_url = reverse_lazy('core:listavenda')

# class EditarClienteView(UpdateView):

#     template_name = 'cliente/cliente_edit.html'
#     success_url = reverse_lazy('core:listacliente')
#     context_object_name = 'cliente'

#     def get_object(self, queryset=None):
#         pk = self.kwargs.get(self.pk_url_kwarg)
#         obj = Cliente.objects.get(pk=pk)
#         return obj

#     def get(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         venda_form = VendaForm(instance=self.object, prefix='venda_form')

#         return self.render_to_response(self.get_context_data(form=venda_form))

#     def post(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         venda_form = VendaForm(
#             request.POST, request.FILES, instance=self.object, prefix='venda_form', request=request)

#         if venda_form.is_valid():
#             self.object = venda_form.save(commit=False)
#             self.object.save()

#             return self.form_valid(venda_form)
#         return self.form_invalid(form=venda_form)
