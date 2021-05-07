from django.contrib.auth.models import User
from django.views.generic.base import TemplateView
from core.forms.Cliente import ClienteForm
from django.urls import reverse_lazy
from django.views.generic import DeleteView, CreateView, ListView, UpdateView

from core.models.cliente import Cliente
from core.models import Imovel


class Index(ListView):

    model = Imovel
    template_name = "base/index.html"
    context_object_name = 'all_imoveis'


class AdicionaClienteView(CreateView):
    template_name = "cliente/criar_cliente.html"
    success_url = reverse_lazy('core:listacliente')
    success_message = "Cliente <b>%(email)s </b>adicionado com sucesso."

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, username=cleaned_data['email'])

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
    # success_url = reverse_lazy('cliente:listpaciente')
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
