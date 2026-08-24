from django.contrib import admin

from .models import (
    Agendamento,
    Servico,
    DisponibilidadeSemanal,
    BloqueioSemanal,
)


@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):

    list_display = (
        "nome",
        "preco",
        "duracao",
    )

    search_fields = (
        "nome",
    )


@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):

    list_display = (
        "nome",
        "telefone",
        "servico",
        "data",
        "horario",
        "status",
        "valor",
    )

    list_filter = (
        "status",
        "data",
        "servico",
    )

    search_fields = (
        "nome",
        "telefone",
    )

    ordering = (
        "data",
        "horario",
    )


@admin.register(DisponibilidadeSemanal)
class DisponibilidadeSemanalAdmin(admin.ModelAdmin):

    list_display = (
        "dia_semana",
        "ativo",
        "horario_inicio",
        "horario_fim",
    )

    list_filter = (
        "ativo",
        "dia_semana",
    )


@admin.register(BloqueioSemanal)
class BloqueioSemanalAdmin(admin.ModelAdmin):

    list_display = (
        "dia_semana",
        "horario_inicio",
        "horario_fim",
        "descricao",
        "ativo",
    )

    list_filter = (
        "ativo",
        "dia_semana",
    )

    search_fields = (
        "descricao",
    )