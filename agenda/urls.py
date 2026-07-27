from django.urls import path
from . import views

urlpatterns = [
    path(
        "",
        views.agendamento,
        name="agendamento",
    ),

    path(
        "horarios/",
        views.horarios_disponiveis,
        name="horarios_disponiveis",
    ),

    path(
        "criar/",
        views.criar_agendamento,
        name="criar_agendamento",
    ),

    path(
        "pagamento/<int:agendamento_id>/",
        views.pagamento,
        name="pagamento",
    ),

    path(
        "sucesso/",
        views.sucesso,
        name="sucesso",
    ),
]