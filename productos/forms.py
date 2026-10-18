from django import forms

from .models import Producto


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ["nombre", "descripcion", "precio", "cantidad_disponible"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "descripcion": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "precio": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "cantidad_disponible": forms.NumberInput(attrs={"class": "form-control", "step": "1"}),
        }

    def clean_nombre(self):
        return self.cleaned_data["nombre"].strip()

    def clean_precio(self):
        precio = self.cleaned_data["precio"]
        if precio is None or precio <= 0:
            raise forms.ValidationError("El precio debe ser mayor que cero.")
        return precio