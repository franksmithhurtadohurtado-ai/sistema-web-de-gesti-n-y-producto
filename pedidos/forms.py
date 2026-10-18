from django import forms

from .models import Pedido


class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        # "usuario" y "fecha_registro" NO se piden: los asigna el servidor
        fields = ["numero_pedido", "cliente", "descripcion", "valor_total", "estado"]
        widgets = {
            "numero_pedido": forms.TextInput(attrs={"class": "form-control"}),
            "cliente": forms.TextInput(attrs={"class": "form-control"}),
            "descripcion": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "valor_total": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "estado": forms.Select(attrs={"class": "form-select"}),
        }

    def clean_numero_pedido(self):
        return self.cleaned_data["numero_pedido"].strip()

    def clean_cliente(self):
        return self.cleaned_data["cliente"].strip()

    def clean_descripcion(self):
        descripcion = self.cleaned_data["descripcion"].strip()
        if not descripcion:
            raise forms.ValidationError("La descripción del pedido es obligatoria.")
        return descripcion

    def clean_valor_total(self):
        valor = self.cleaned_data["valor_total"]
        if valor is None or valor <= 0:
            raise forms.ValidationError("El valor total debe ser mayor que cero.")
        return valor