from datetime import datetime, date

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .models import Agendamento, Servico
from .utils import gerar_horarios


def agendamento(request):

    servicos = Servico.objects.all()

    data = request.GET.get("data")

    horarios = gerar_horarios()

    if data:

        ocupados = Agendamento.objects.filter(
            data=data,
            status__in=[
                "PENDENTE",
                "CONFIRMADO",
                "FINALIZADO",
            ],
        ).values_list(
            "horario",
            flat=True,
        )

        ocupados = [
            horario.strftime("%H:%M")
            for horario in ocupados
        ]

        horarios = [
            horario
            for horario in horarios
            if horario not in ocupados
        ]

    return render(
        request,
        "agenda/agendamento.html",
        {
            "servicos": servicos,
            "horarios": horarios,
            "hoje": date.today(),
        },
    )


def horarios_disponiveis(request):

    data = request.GET.get("data")

    horarios = gerar_horarios()

    if data:

        ocupados = Agendamento.objects.filter(
            data=data,
            status__in=[
                "PENDENTE",
                "CONFIRMADO",
                "FINALIZADO",
            ],
        ).values_list(
            "horario",
            flat=True,
        )

        ocupados = [
            horario.strftime("%H:%M")
            for horario in ocupados
        ]

        horarios = [
            horario
            for horario in horarios
            if horario not in ocupados
        ]

    return JsonResponse(
        {
            "horarios": horarios,
        }
    )


def criar_agendamento(request):

    if request.method != "POST":
        return redirect("agendamento")

    data_agendamento = datetime.strptime(
        request.POST.get("data"),
        "%Y-%m-%d",
    ).date()

    if data_agendamento < date.today():
        return redirect("agendamento")

    servico = get_object_or_404(
        Servico,
        id=request.POST.get("servico"),
    )

    horario = request.POST.get("horario")

    existe = Agendamento.objects.filter(
        data=data_agendamento,
        horario=horario,
        status__in=[
            "PENDENTE",
            "CONFIRMADO",
            "FINALIZADO",
        ],
    ).exists()

    if existe:
        return redirect("agendamento")

    Agendamento.objects.create(
        nome=request.POST.get("nome"),
        telefone=request.POST.get("telefone"),
        servico=servico,
        data=data_agendamento,
        horario=horario,
        valor=servico.preco,
        status="PENDENTE",
    )

    return redirect("sucesso")


def sucesso(request):

    return render(
        request,
        "agenda/sucesso.html",
    )


@login_required(login_url="/login/")
def painel_agendamentos(request):

    agendamentos = Agendamento.objects.all().order_by(
        "data",
        "horario",
    )

    return render(
        request,
        "agenda/painel.html",
        {
            "agendamentos": agendamentos,
        },
    )


@login_required(login_url="/login/")
def confirmar_agendamento(request, id):

    agendamento = get_object_or_404(
        Agendamento,
        id=id,
    )

    agendamento.status = "CONFIRMADO"
    agendamento.save()

    return redirect("painel_agendamentos")


@login_required(login_url="/login/")
def finalizar_agendamento(request, id):

    agendamento = get_object_or_404(
        Agendamento,
        id=id,
    )

    agendamento.status = "FINALIZADO"
    agendamento.save()

    return redirect("painel_agendamentos")


@login_required(login_url="/login/")
def cancelar_agendamento(request, id):

    agendamento = get_object_or_404(
        Agendamento,
        id=id,
    )

    agendamento.status = "CANCELADO"
    agendamento.save()

    return redirect("painel_agendamentos")


@login_required(login_url="/login/")
def excluir_agendamento(request, id):

    agendamento = get_object_or_404(
        Agendamento,
        id=id,
    )

    agendamento.delete()

    return redirect("painel_agendamentos")