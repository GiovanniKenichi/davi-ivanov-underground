from datetime import datetime, date

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .models import (
    Agendamento,
    Servico,
    DisponibilidadeSemanal,
    BloqueioSemanal,
)

from .utils import gerar_horarios


def obter_horarios_disponiveis(data):

    # ==========================================
    # HORÁRIOS PADRÃO
    # ==========================================

    horarios = gerar_horarios()

    # ==========================================
    # DISPONIBILIDADE DO DIA DA SEMANA
    # ==========================================

    dia_semana = data.weekday()

    disponibilidade = DisponibilidadeSemanal.objects.filter(
        dia_semana=dia_semana
    ).first()

    # Se existir configuração para o dia
    if disponibilidade:

        # Se o dia estiver desativado, não há horários
        if not disponibilidade.ativo:
            return []

        inicio = disponibilidade.horario_inicio.strftime("%H:%M")
        fim = disponibilidade.horario_fim.strftime("%H:%M")

        horarios = [
            horario
            for horario in horarios
            if inicio <= horario <= fim
        ]

    # ==========================================
    # BLOQUEIOS SEMANAIS
    # ==========================================

    bloqueios = BloqueioSemanal.objects.filter(
        dia_semana=dia_semana,
        ativo=True,
    )

    horarios_bloqueados = []

    for bloqueio in bloqueios:

        inicio = bloqueio.horario_inicio
        fim = bloqueio.horario_fim

        horarios_bloqueados.append(
            (inicio, fim)
        )

    horarios_filtrados = []

    for horario in horarios:

        horario_obj = datetime.strptime(
            horario,
            "%H:%M",
        ).time()

        bloqueado = False

        for inicio, fim in horarios_bloqueados:

            if inicio <= horario_obj < fim:
                bloqueado = True
                break

        if not bloqueado:
            horarios_filtrados.append(
                horario
            )

    horarios = horarios_filtrados

    # ==========================================
    # AGENDAMENTOS JÁ EXISTENTES
    # ==========================================

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

    return horarios


# ==========================================
# PÁGINA DE AGENDAMENTO
# ==========================================

def agendamento(request):

    servicos = Servico.objects.all()

    data = request.GET.get("data")

    horarios = gerar_horarios()

    if data:

        try:

            data_obj = datetime.strptime(
                data,
                "%Y-%m-%d",
            ).date()

            horarios = obter_horarios_disponiveis(
                data_obj
            )

        except (ValueError, TypeError):

            horarios = []

    return render(
        request,
        "agenda/agendamento.html",
        {
            "servicos": servicos,
            "horarios": horarios,
            "hoje": date.today(),
        },
    )


# ==========================================
# HORÁRIOS DISPONÍVEIS - AJAX
# ==========================================

def horarios_disponiveis(request):

    data = request.GET.get("data")

    if not data:

        return JsonResponse(
            {
                "horarios": gerar_horarios()
            }
        )

    try:

        data_obj = datetime.strptime(
            data,
            "%Y-%m-%d",
        ).date()

    except (ValueError, TypeError):

        return JsonResponse(
            {
                "horarios": []
            }
        )

    horarios = obter_horarios_disponiveis(
        data_obj
    )

    return JsonResponse(
        {
            "horarios": horarios
        }
    )


# ==========================================
# CRIAR AGENDAMENTO
# ==========================================

def criar_agendamento(request):

    if request.method != "POST":

        return redirect(
            "agendamento"
        )

    try:

        data_agendamento = datetime.strptime(
            request.POST.get("data"),
            "%Y-%m-%d",
        ).date()

    except (ValueError, TypeError):

        return redirect(
            "agendamento"
        )

    if data_agendamento < date.today():

        return redirect(
            "agendamento"
        )

    servico = get_object_or_404(
        Servico,
        id=request.POST.get("servico"),
    )

    horario = request.POST.get(
        "horario"
    )

    # ==========================================
    # VERIFICA SE O HORÁRIO ESTÁ DISPONÍVEL
    # ==========================================

    horarios_disponiveis_lista = (
        obter_horarios_disponiveis(
            data_agendamento
        )
    )

    if horario not in horarios_disponiveis_lista:

        return redirect(
            "agendamento"
        )

    # ==========================================
    # VERIFICA DUPLICIDADE
    # ==========================================

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

        return redirect(
            "agendamento"
        )

    # ==========================================
    # CRIA AGENDAMENTO
    # ==========================================

    Agendamento.objects.create(
        nome=request.POST.get(
            "nome"
        ),
        telefone=request.POST.get(
            "telefone"
        ),
        servico=servico,
        data=data_agendamento,
        horario=horario,
        valor=servico.preco,
        status="PENDENTE",
    )

    return redirect(
        "sucesso"
    )


# ==========================================
# SUCESSO
# ==========================================

def sucesso(request):

    return render(
        request,
        "agenda/sucesso.html",
    )


# ==========================================
# PAINEL DE AGENDAMENTOS
# ==========================================

@login_required(login_url="/login/")
def painel_agendamentos(request):

    agendamentos = (
        Agendamento.objects.all()
        .order_by(
            "data",
            "horario",
        )
    )

    return render(
        request,
        "agenda/painel.html",
        {
            "agendamentos": agendamentos,
        },
    )


# ==========================================
# CONFIRMAR
# ==========================================

@login_required(login_url="/login/")
def confirmar_agendamento(
    request,
    id,
):

    agendamento = get_object_or_404(
        Agendamento,
        id=id,
    )

    agendamento.status = "CONFIRMADO"

    agendamento.save()

    return redirect(
        "painel_agendamentos"
    )


# ==========================================
# FINALIZAR
# ==========================================

@login_required(login_url="/login/")
def finalizar_agendamento(
    request,
    id,
):

    agendamento = get_object_or_404(
        Agendamento,
        id=id,
    )

    agendamento.status = "FINALIZADO"

    agendamento.save()

    return redirect(
        "painel_agendamentos"
    )


# ==========================================
# CANCELAR
# ==========================================

@login_required(login_url="/login/")
def cancelar_agendamento(
    request,
    id,
):

    agendamento = get_object_or_404(
        Agendamento,
        id=id,
    )

    agendamento.status = "CANCELADO"

    agendamento.save()

    return redirect(
        "painel_agendamentos"
    )


# ==========================================
# EXCLUIR
# ==========================================

@login_required(login_url="/login/")
def excluir_agendamento(
    request,
    id,
):

    agendamento = get_object_or_404(
        Agendamento,
        id=id,
    )

    agendamento.delete()

    return redirect(
        "painel_agendamentos"
    )