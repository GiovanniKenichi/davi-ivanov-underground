from django.urls import path

from . import views


urlpatterns = [

    # ==========================================
    # AGENDAMENTO DO CLIENTE
    # ==========================================

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
        "sucesso/",
        views.sucesso,
        name="sucesso",
    ),

    # ==========================================
    # PAINEL DE AGENDAMENTOS
    # ==========================================

    path(
        "painel/",
        views.painel_agendamentos,
        name="painel_agendamentos",
    ),

    path(
        "confirmar/<int:id>/",
        views.confirmar_agendamento,
        name="confirmar_agendamento",
    ),

    path(
        "finalizar/<int:id>/",
        views.finalizar_agendamento,
        name="finalizar_agendamento",
    ),

    path(
        "cancelar/<int:id>/",
        views.cancelar_agendamento,
        name="cancelar_agendamento",
    ),

    path(
        "excluir/<int:id>/",
        views.excluir_agendamento,
        name="excluir_agendamento",
    ),

    # ==========================================
    # CONFIGURAÇÃO DE HORÁRIOS
    # ==========================================

    path(
        "disponibilidade/<int:dia_semana>/",
        views.salvar_disponibilidade,
        name="salvar_disponibilidade",
    ),

    path(
        "bloqueio/criar/",
        views.criar_bloqueio,
        name="criar_bloqueio",
    ),

    path(
        "bloqueio/remover/<int:id>/",
        views.remover_bloqueio,
        name="remover_bloqueio",
    ),
]