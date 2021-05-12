from django.views.generic import DeleteView, CreateView, ListView, UpdateView
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from decimal import Decimal

from core.models import Venda, Cliente
from core.forms import VendaForm


# Função para verificar parametro para filtro
def is_valid_queryparam(param):
    return param != '' and param is not None


# Classe responsável por listar todas as vendas
class ListaClienteVendaView(ListView):

    template_name = "venda/lista_venda.html"
    context_object_name = 'vendas'

    def get_queryset(self):
        queryset = Venda.objects.filter(vendedor_user=self.request.user)
        return queryset

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()

        vendas_finalizadas = request.GET.get('vendas_finalizadas')
        vendas_aguardando = request.GET.get('vendas_aguardando')
        clientes = request.GET.get('clientes')

        # Filtar todas vendas finalizadas
        if is_valid_queryparam(vendas_finalizadas):
            self.object_list = self.object_list.filter(venda_status=True)

        # Filtar todas vendas não finalizadas
        if is_valid_queryparam(vendas_aguardando):
            self.object_list = self.object_list.filter(venda_status=False)

        # Filtar vendas de um específico
        if is_valid_queryparam(clientes) and clientes != 'Todos':
            self.object_list = self.object_list.filter(
                cliente_cliente__email=clientes)

        return self.render_to_response(self.get_context_data())

    def get_context_data(self, **kwargs):
        context = super(ListaClienteVendaView, self).get_context_data(**kwargs)
        context['add_url'] = reverse_lazy('core:addvenda')
        context['todos_clientes'] = Cliente.objects.filter(
            criado_por=self.request.user)
        return context


# Classe responsável por adicionar uma venda no sistema
class AdicionarVendaView(CreateView):

    template_name = "venda/criar_venda.html"
    model = Venda
    success_message = "Venda cadastrada, porém, não finalizada para o cliente <b>%(descricao)s </b>."

    # Função responsável por pegar o id da venda criada e encaminha para o CheckoutView
    def get_success_url(self):
        success_url = reverse('core:checkout', kwargs={
            'pk': self.object.pk,
        })
        return success_url

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, descricao=str(self.object.cliente_cliente))

    def form_valid(self, form):
        messages.success(
            self.request, self.get_success_message(form.cleaned_data))
        return redirect(self.get_success_url())

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


# Classe responsável para conferir e salvar, finalizar ou cancelar a venda
class CheckoutView(UpdateView):

    template_name = 'venda/checkout_venda.html'
    context_object_name = 'all_vendas'
    success_url = reverse_lazy('core:listavenda')
    success_message = "Venda para o cliente <b>%(descricao)s </b> <b>finalizada</b> com sucesso."

    def get_success_message(self):
        return self.success_message % dict(descricao=str(self.object.cliente_cliente.email))

    def form_valid(self):
        messages.success(
            self.request, self.get_success_message())
        return redirect(self.success_url)

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

        return self.form_valid()


class DeletarVendaView(DeleteView):

    template_name = 'venda/venda_confirm_delete.html'
    model = Venda
    success_url = reverse_lazy('core:listavenda')
