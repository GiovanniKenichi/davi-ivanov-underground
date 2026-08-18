from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from agenda.models import Agendamento


# ==========================================
# HOME
# ==========================================

def home(request):

    return render(
        request,
        "core/home.html",
    )


# ==========================================
# LOGIN
# ==========================================

def login_admin(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    erro = None

    if request.method == "POST":

        usuario = request.POST.get("usuario")
        senha = request.POST.get("senha")

        user = authenticate(
            request,
            username=usuario,
            password=senha,
        )

        if user is not None:

            login(request, user)

            return redirect("dashboard")

        erro = "Usuário ou senha inválidos."

    return render(
        request,
        "dashboard/login.html",
        {
            "erro": erro,
        },
    )


# ==========================================
# DASHBOARD
# ==========================================

@login_required(login_url="/login/")
def dashboard(request):

    agendamentos = Agendamento.objects.all()

    total = agendamentos.count()

    pendentes = agendamentos.filter(
        status="PENDENTE"
    ).count()

    confirmados = agendamentos.filter(
        status="CONFIRMADO"
    ).count()

    finalizados = agendamentos.filter(
        status="FINALIZADO"
    ).count()

    cancelados = agendamentos.filter(
        status="CANCELADO"
    ).count()

    faturamento = sum(

        item.valor

        for item in agendamentos.filter(
            status__in=[
                "CONFIRMADO",
                "FINALIZADO",
            ]
        )

    )

    ultimos = agendamentos.order_by(
        "-criado_em"
    )[:5]

    return render(
        request,
        "dashboard/dashboard.html",
        {
            "total": total,
            "pendentes": pendentes,
            "confirmados": confirmados,
            "finalizados": finalizados,
            "cancelados": cancelados,
            "faturamento": faturamento,
            "ultimos": ultimos,
        },
    )


# ==========================================
# LOGOUT
# ==========================================

@login_required(login_url="/login/")
def sair(request):

    logout(request)

    return redirect("login")