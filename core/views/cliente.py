from django.shortcuts import redirect
from django.urls.base import reverse_lazy
from django.views.generic import DeleteView, CreateView, ListView, UpdateView
from django.contrib import messages

from core.models.venda import Venda
from core.forms.Cliente import ClienteForm
from core.models import Imovel, Cliente


# Classe responsável por renderizar a tela de home
# mostrando somente os imaveis qua estão disponiveis
class Index(ListView):

    template_name = "base/index.html"
    context_object_name = 'all_imoveis'

    def get_queryset(self):
        queryset = Imovel.objects.filter(vendido_status=False)
        return queryset


class AdicionaClienteView(CreateView):

    template_name = "cliente/criar_cliente.html"
    success_url = reverse_lazy('core:listacliente')
    success_message = "Cliente <b>%(descricao)s </b> adicionado com sucesso."

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, descricao=str(self.object))

    def form_valid(self, form):
        messages.success(
            self.request, self.get_success_message(form.cleaned_data))
        return redirect(self.get_success_url())

    def get(self, request, *args, **kwargs):
        self.object = None

        cliente_form = ClienteForm(prefix='cliente_form')

        return self.render_to_response(self.get_context_data(form=cliente_form))

    def post(self, request, *args, **kwargs):
        self.object = None

        cliente_form = ClienteForm(
            request.POST, request.FILES, prefix='cliente_form', request=request)

        if cliente_form.is_valid():
            self.object = cliente_form.save(commit=False)
            self.object.save()

            return self.form_valid(cliente_form)

        return self.form_invalid(form=cliente_form)


class ListarClienteView(ListView):

    template_name = 'cliente/cliente_list.html'
    context_object_name = 'all_clientes'

    def get_queryset(self):
        queryset = Cliente.objects.filter(criado_por=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ListarClienteView, self).get_context_data(**kwargs)
        context['add_url'] = reverse_lazy('core:addcliente')
        return context


class EditarClienteView(UpdateView):

    template_name = 'cliente/cliente_edit.html'
    success_url = reverse_lazy('core:listacliente')
    context_object_name = 'cliente'
    success_message = "Dados do cliente <b>%(descricao)s </b> editados com sucesso."

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, descricao=str(self.object))

    def form_valid(self, form):
        messages.success(
            self.request, self.get_success_message(form.cleaned_data))
        return redirect(self.get_success_url())

    def get_object(self, queryset=None):
        pk = self.kwargs.get(self.pk_url_kwarg)
        obj = Cliente.objects.get(pk=pk)
        return obj

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        cliente_form = ClienteForm(instance=self.object, prefix='cliente_form')

        return self.render_to_response(self.get_context_data(form=cliente_form))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        cliente_form = ClienteForm(
            request.POST, request.FILES, instance=self.object, prefix='cliente_form', request=request)

        if cliente_form.is_valid():
            self.object = cliente_form.save(commit=False)
            self.object.save()

            return self.form_valid(cliente_form)
        return self.form_invalid(form=cliente_form)


class DeletarClienteView(DeleteView):

    template_name = 'cliente/cliente_confirm_delete.html'
    model = Cliente
    success_url = reverse_lazy('core:listacliente')

    def get_queryset(self):
        x = self.kwargs.get(self.pk_url_kwarg)
        queryset = Cliente.objects.all()
        return queryset

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        teste = Venda.objects.filter(cliente_cliente=self.object)

        if teste:
            return redirect('core:listacliente')

        return self.render_to_response(context)
