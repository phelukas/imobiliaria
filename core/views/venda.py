from django.views.generic import DeleteView, CreateView, ListView, UpdateView
import json

from django.views.generic.base import View

from core.models import Imovel, Venda, Cliente
from core.forms import VendaForm, ClienteForm

from django.http import HttpResponse, response


class ListaClienteVendaView(View):

    model = Cliente

    def post(self, request, *args, **kwargs):
        response = json.dumps({'mensagem':'Requisição '})
        return HttpResponse(response, content_type='application/json')


class AdicionarVendaView(CreateView):

    template_name = "base/simulacao.html"
    queryset = Cliente.objects.all()
    
    def get(self, request, *args, **kwargs):
        self.object = Cliente.objects.all()
        print(self.object)

        venda_form = VendaForm(prefix='venda_form')
        cliente_form = ClienteForm(prefix='cliente_form')

        return self.render_to_response(self.get_context_data(form=venda_form, form2=cliente_form))

# class AdicionaClienteView(CreateView):
#     template_name = "cliente/criar_cliente.html"
#     success_url = reverse_lazy('core:listacliente')
#     success_message = "Cliente <b>%(email)s </b>adicionado com sucesso."

#     def get_success_message(self, cleaned_data):
#         return self.success_message % dict(cleaned_data, username=cleaned_data['email'])

#     def get(self, request, *args, **kwargs):
#         self.object = None

#         venda_form = VendaForm(prefix='venda_form')

#         return self.render_to_response(self.get_context_data(form=venda_form))

#     def post(self, request, *args, **kwargs):
#         self.object = None

#         venda_form = VendaForm(
#             request.POST, request.FILES, prefix='venda_form', request=request)

#         if venda_form.is_valid():
#             self.object = venda_form.save(commit=False)
#             self.object.save()

#             return self.form_valid(venda_form)

#         return self.form_invalid(form=venda_form)


# class ListarClienteView(ListView):

#     template_name = 'cliente/cliente_list.html'
#     # success_url = reverse_lazy('cliente:listpaciente')
#     context_object_name = 'all_clientes'

#     def get_queryset(self):
#         queryset = Cliente.objects.filter(criado_por=self.request.user)
#         return queryset

#     def get_context_data(self, **kwargs):
#         context = super(ListarClienteView, self).get_context_data(**kwargs)
#         context['add_url'] = reverse_lazy('core:addcliente')
#         return context


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
