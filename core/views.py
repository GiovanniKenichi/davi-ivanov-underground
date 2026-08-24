import os

from django.contrib.auth import authenticate, login, logout, get_user_model
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


# ==========================================
# RECUPERAÇÃO TEMPORÁRIA DO ADMIN
# ==========================================

def recuperar_admin(request):

    token_url = request.GET.get("token")

    token_correto = os.environ.get(
        "ADMIN_RESET_TOKEN"
    )

    nova_senha = os.environ.get(
        "ADMIN_NEW_PASSWORD"
    )

    if not token_correto or not nova_senha:

        return render(
            request,
            "dashboard/reset_result.html",
            {
                "mensagem": "Recuperação não configurada."
            },
        )

    if token_url != token_correto:

        return render(
            request,
            "dashboard/reset_result.html",
            {
                "mensagem": "Token inválido."
            },
        )

    User = get_user_model()

    try:

        usuario = User.objects.get(
            username="admin"
        )

    except User.DoesNotExist:

        return render(
            request,
            "dashboard/reset_result.html",
            {
                "mensagem": "Usuário admin não encontrado."
            },
        )

    usuario.set_password(
        nova_senha
    )

    usuario.is_staff = True
    usuario.is_superuser = True
    usuario.is_active = True

    usuario.save()

    return render(
        request,
        "dashboard/reset_result.html",
        {
            "mensagem": (
                "Senha do administrador alterada "
                "com sucesso."
            )
        },
    )