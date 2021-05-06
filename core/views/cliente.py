from django.views.generic.base import TemplateView
from core.forms.Cliente import ClienteForm
from django.urls import reverse_lazy
from django.views.generic import DeleteView, CreateView, ListView, UpdateView

from core.models.cliente import Cliente


class Index(TemplateView):
    template_name = "base/index.html"



class AdicionaClienteView(CreateView):
    # template_name = "paciente/criar_paciente.html"
    # success_url = reverse_lazy('cliente:listpaciente')
    success_message = "Cliente <b>%(email)s </b>adicionado com sucesso."

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, username=cleaned_data['email'])

    def get(self, request, *args, **kwargs):
        self.object = None

        paciente_form = Cliente(prefix='paciente_form')

        return self.render_to_response(self.get_context_data(form=paciente_form))

    def post(self, request, *args, **kwargs):
        self.object = None

        paciente_form = ClienteForm(request.POST, request.FILES, prefix='cliente_form', request=request)


        if paciente_form.is_valid():
            self.object = paciente_form.save(commit=False)
            self.object.save()

            return self.form_valid(paciente_form)

        return self.form_invalid(form=paciente_form)


class ListarClienteView(ListView):

    template_name = 'paciente/paciente_list.html'
    # success_url = reverse_lazy('cliente:listpaciente')
    # context_object_name = 'all_clientes'

    def get_queryset(self):
        queryset = Cliente.objects.filter(criado_por=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ListarClienteView, self).get_context_data(**kwargs)
        return context


# class EditarPacienteView(CustomUpdateView):

#     template_name = 'paciente/paciente_edit.html'
#     success_url = reverse_lazy('cliente:listpaciente')
#     success_message = "Informações do paciente <b>%(email)s </b>editada com sucesso."

#     def get_object(self, queryset=None):
#         pk = self.kwargs.get(self.pk_url_kwarg)
#         obj = Endereco_pacientes.objects.select_related(
#             'paciente_end').get(paciente_end=pk)
#         return obj

#     def get_success_message(self, cleaned_data):
#         return self.success_message % dict(cleaned_data, username=cleaned_data['email'])

#     def get_context_data(self, **kwargs):
#         context = super(EditarPacienteView, self).get_context_data(**kwargs)
#         context['return_url'] = reverse_lazy('cliente:listpaciente')
#         return context

#     def get(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         paciente_form = PacientesForm(
#             instance=self.object.paciente_end, prefix='paciente_form')
#         endereco_form = EnderecoForm(
#             instance=self.object, prefix='endereco_form')

#         return self.render_to_response(self.get_context_data(form=paciente_form, form2=endereco_form))

#     def post(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         paciente_form = PacientesForm(
#             request.POST, request.FILES, instance=self.object.paciente_end, prefix='paciente_form', request=request)

#         endereco_form = EnderecoForm(
#             request.POST, request.FILES, instance=self.object, prefix='endereco_form', request=request)

#         if paciente_form.is_valid() and endereco_form.is_valid():
#             self.object = paciente_form.save(commit=False)
#             self.object.save()
#             self.object = endereco_form.save(commit=False)
#             self.object.save()
#             return self.form_valid(paciente_form)
#         return self.form_invalid(form=paciente_form, form2=endereco_form)


# class DeletarPacienteView(DeleteView):

#     template_name = 'paciente/pacientes_confirm_delete.html'
#     model = Pacientes
#     success_url = reverse_lazy('cliente:listpaciente')