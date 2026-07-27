from datetime import datetime, date

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
            status__in=["PENDENTE", "PAGO", "FINALIZADO"]
        ).values_list("horario", flat=True)

        ocupados = [
            horario.strftime("%H:%M")
            for horario in ocupados
        ]

        horarios = [
            horario
            for horario in horarios
            if horario not in ocupados
        ]

    context = {
        "servicos": servicos,
        "horarios": horarios,
        "hoje": date.today(),
    }

    return render(
        request,
        "agenda/agendamento.html",
        context
    )


def horarios_disponiveis(request):
    data = request.GET.get("data")

    horarios = gerar_horarios()

    if data:
        ocupados = Agendamento.objects.filter(
            data=data,
            status__in=["PENDENTE", "PAGO", "FINALIZADO"]
        ).values_list("horario", flat=True)

        ocupados = [
            horario.strftime("%H:%M")
            for horario in ocupados
        ]

        horarios = [
            horario
            for horario in horarios
            if horario not in ocupados
        ]

    return JsonResponse({
        "horarios": horarios
    })


def criar_agendamento(request):
    if request.method != "POST":
        return redirect("agendamento")

    data_agendamento = datetime.strptime(
        request.POST.get("data"),
        "%Y-%m-%d"
    ).date()

    if data_agendamento < date.today():
        return redirect("agendamento")

    servico = get_object_or_404(
        Servico,
        id=request.POST.get("servico")
    )

    horario = request.POST.get("horario")

    # Impede dois clientes de agendarem o mesmo horário
    existe = Agendamento.objects.filter(
        data=data_agendamento,
        horario=horario,
        status__in=["PENDENTE", "PAGO", "FINALIZADO"]
    ).exists()

    if existe:
        return redirect("agendamento")

    agendamento = Agendamento.objects.create(
        nome=request.POST.get("nome"),
        telefone=request.POST.get("telefone"),
        servico=servico,
        data=data_agendamento,
        horario=horario,
        valor=servico.preco,
    )

    return redirect(
        "pagamento",
        agendamento.id
    )


def pagamento(request, agendamento_id):
    agendamento = get_object_or_404(
        Agendamento,
        id=agendamento_id
    )

    return render(
        request,
        "agenda/pagamento.html",
        {
            "agendamento": agendamento
        }
    )


def sucesso(request):
    return render(
        request,
        "agenda/sucesso.html"
    )