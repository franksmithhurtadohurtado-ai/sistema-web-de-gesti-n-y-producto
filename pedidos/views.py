from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import PedidoForm
from .models import Pedido


class PedidoListView(LoginRequiredMixin, ListView):
    model = Pedido
    template_name = "pedidos/lista.html"
    context_object_name = "pedidos"
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset().select_related("usuario")
        q = self.request.GET.get("q", "").strip()
        if q:
            qs = qs.filter(cliente__icontains=q)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["q"] = self.request.GET.get("q", "").strip()
        return ctx


class PedidoDetailView(LoginRequiredMixin, DetailView):
    model = Pedido
    template_name = "pedidos/detalle.html"


class PedidoCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Pedido
    form_class = PedidoForm
    template_name = "pedidos/form.html"
    success_url = reverse_lazy("pedidos:lista")
    success_message = "Pedido registrado correctamente."

    def form_valid(self, form):
        # El usuario autenticado queda asociado al pedido que registra
        form.instance.usuario = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Revisa los campos marcados en rojo.")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["titulo"] = "Nuevo pedido"
        return ctx


class PedidoUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Pedido
    form_class = PedidoForm
    template_name = "pedidos/form.html"
    success_url = reverse_lazy("pedidos:lista")
    success_message = "Pedido actualizado correctamente."

    def form_invalid(self, form):
        messages.error(self.request, "Revisa los campos marcados en rojo.")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["titulo"] = "Editar pedido"
        return ctx


class PedidoDeleteView(LoginRequiredMixin, DeleteView):
    model = Pedido
    template_name = "pedidos/confirmar_eliminar.html"
    success_url = reverse_lazy("pedidos:lista")

    def form_valid(self, form):
        messages.success(self.request, "Pedido eliminado correctamente.")
        return super().form_valid(form)


@login_required
@require_POST
def cambiar_estado(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    nuevo = request.POST.get("estado")
    # Validación en servidor: solo se aceptan los estados definidos en el modelo
    if nuevo not in dict(Pedido.ESTADOS):
        messages.error(request, "Estado no válido.")
    else:
        pedido.estado = nuevo
        pedido.save(update_fields=["estado"])
        messages.success(request, f"El pedido {pedido.numero_pedido} ahora está {pedido.get_estado_display().lower()}.")
    destino = request.POST.get("next", "")
    if destino and url_has_allowed_host_and_scheme(destino, allowed_hosts={request.get_host()}):
        return redirect(destino)
    return redirect("pedidos:lista")