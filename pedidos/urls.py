from django.urls import path

from . import views

app_name = "pedidos"

urlpatterns = [
    path("", views.PedidoListView.as_view(), name="lista"),
    path("nuevo/", views.PedidoCreateView.as_view(), name="crear"),
    path("<int:pk>/", views.PedidoDetailView.as_view(), name="detalle"),
    path("<int:pk>/editar/", views.PedidoUpdateView.as_view(), name="editar"),
    path("<int:pk>/eliminar/", views.PedidoDeleteView.as_view(), name="eliminar"),
    path("<int:pk>/estado/", views.cambiar_estado, name="cambiar_estado"),
]