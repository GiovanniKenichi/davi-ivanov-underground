from django.contrib import admin
from django.utils.html import format_html

from .models import Servico, Agendamento


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

    ordering = (
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
        "valor",
        "status_colorido",
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
        "-data",
        "horario",
    )

    date_hierarchy = "data"

    readonly_fields = (
        "valor",
    )

    fieldsets = (

        ("Cliente", {
            "fields": (
                "nome",
                "telefone",
            )
        }),

        ("Agendamento", {
            "fields": (
                "servico",
                "data",
                "horario",
            )
        }),

        ("Informações", {
            "fields": (
                "valor",
                "status",
            )
        }),

    )

    actions = [
        "marcar_confirmado",
        "marcar_finalizado",
        "marcar_cancelado",
    ]

    def status_colorido(self, obj):

        cores = {
            "PENDENTE": "#f1c40f",
            "CONFIRMADO": "#2ecc71",
            "FINALIZADO": "#3498db",
            "CANCELADO": "#e74c3c",
        }

        cor = cores.get(obj.status, "#999")

        return format_html(
            '<strong style="color:{};">{}</strong>',
            cor,
            obj.status
        )

    status_colorido.short_description = "Status"

    @admin.action(description="Marcar como Confirmado")
    def marcar_confirmado(self, request, queryset):

        queryset.update(status="CONFIRMADO")

    @admin.action(description="Marcar como Finalizado")
    def marcar_finalizado(self, request, queryset):

        queryset.update(status="FINALIZADO")

    @admin.action(description="Marcar como Cancelado")
    def marcar_cancelado(self, request, queryset):

        queryset.update(status="CANCELADO")