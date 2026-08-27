from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from agenda.models import Servico


class Command(BaseCommand):

    help = "Cria os serviços e o administrador inicial"

    def handle(self, *args, **kwargs):

        # ==========================================
        # SERVIÇOS
        # ==========================================

        servicos = [
            {
                "nome": "BARBA",
                "preco": 45.00,
                "duracao": 30,
                "descricao": "Serviço profissional de barba.",
            },
            {
                "nome": "CORTE DE CABELO",
                "preco": 45.00,
                "duracao": 45,
                "descricao": "Corte de cabelo profissional.",
            },
            {
                "nome": "CORTE+BARBA",
                "preco": 80.00,
                "duracao": 60,
                "descricao": "Corte de cabelo + barba.",
            },
        ]

        for dados in servicos:

            Servico.objects.update_or_create(
                nome=dados["nome"],
                defaults={
                    "preco": dados["preco"],
                    "duracao": dados["duracao"],
                    "descricao": dados["descricao"],
                },
            )

            self.stdout.write(
                self.style.SUCCESS(
                    f'Serviço "{dados["nome"]}" configurado.'
                )
            )

        # ==========================================
        # ADMINISTRADOR
        # ==========================================

        User = get_user_model()

        usuario, criado = User.objects.get_or_create(
            username="admin"
        )

        usuario.is_staff = True
        usuario.is_superuser = True
        usuario.is_active = True

        usuario.set_password("Davi@2026Admin")

        usuario.save()

        self.stdout.write(
            self.style.SUCCESS(
                "Administrador configurado com sucesso."
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                "Usuário: admin"
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                "Senha: Davi@2026Admin"
            )
        )