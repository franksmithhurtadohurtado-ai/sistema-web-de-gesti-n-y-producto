from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import ProductoForm
from .models import Producto


class ProductoListView(LoginRequiredMixin, ListView):
    model = Producto
    template_name = "productos/lista.html"
    context_object_name = "productos"
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get("q", "").strip()
        if q:
            qs = qs.filter(nombre__icontains=q)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["q"] = self.request.GET.get("q", "").strip()
        return ctx


class ProductoDetailView(LoginRequiredMixin, DetailView):
    model = Producto
    template_name = "productos/detalle.html"


class ProductoCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = "productos/form.html"
    success_url = reverse_lazy("productos:lista")
    success_message = "Producto creado correctamente."

    def form_invalid(self, form):
        messages.error(self.request, "Revisa los campos marcados en rojo.")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["titulo"] = "Nuevo producto"
        return ctx


class ProductoUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = "productos/form.html"
    success_url = reverse_lazy("productos:lista")
    success_message = "Producto actualizado correctamente."

    def form_invalid(self, form):
        messages.error(self.request, "Revisa los campos marcados en rojo.")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["titulo"] = "Editar producto"
        return ctx


class ProductoDeleteView(LoginRequiredMixin, DeleteView):
    model = Producto
    template_name = "productos/confirmar_eliminar.html"
    success_url = reverse_lazy("productos:lista")

    def form_valid(self, form):
        messages.success(self.request, "Producto eliminado correctamente.")
        return super().form_valid(form)