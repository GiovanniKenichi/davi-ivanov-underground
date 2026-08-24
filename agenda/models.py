from django.db import models


class Servico(models.Model):

    nome = models.CharField(
        max_length=100
    )

    descricao = models.TextField(
        blank=True
    )

    preco = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )

    duracao = models.PositiveIntegerField(
        default=45,
        verbose_name="Duração (minutos)"
    )

    def __str__(self):
        return self.nome


class DisponibilidadeSemanal(models.Model):

    DIAS_SEMANA = [
        (0, "Segunda-feira"),
        (1, "Terça-feira"),
        (2, "Quarta-feira"),
        (3, "Quinta-feira"),
        (4, "Sexta-feira"),
        (5, "Sábado"),
        (6, "Domingo"),
    ]

    dia_semana = models.PositiveSmallIntegerField(
        choices=DIAS_SEMANA,
        unique=True
    )

    ativo = models.BooleanField(
        default=True,
        verbose_name="Atende neste dia"
    )

    horario_inicio = models.TimeField(
        default="09:00",
        verbose_name="Início"
    )

    horario_fim = models.TimeField(
        default="18:00",
        verbose_name="Fim"
    )

    def __str__(self):

        dia = dict(self.DIAS_SEMANA).get(
            self.dia_semana
        )

        if not self.ativo:
            return f"{dia} - Fechado"

        return (
            f"{dia} - "
            f"{self.horario_inicio.strftime('%H:%M')} "
            f"às "
            f"{self.horario_fim.strftime('%H:%M')}"
        )

    class Meta:

        ordering = [
            "dia_semana"
        ]

        verbose_name = "Disponibilidade Semanal"

        verbose_name_plural = "Disponibilidade Semanal"


class BloqueioSemanal(models.Model):

    DIAS_SEMANA = [
        (0, "Segunda-feira"),
        (1, "Terça-feira"),
        (2, "Quarta-feira"),
        (3, "Quinta-feira"),
        (4, "Sexta-feira"),
        (5, "Sábado"),
        (6, "Domingo"),
    ]

    dia_semana = models.PositiveSmallIntegerField(
        choices=DIAS_SEMANA,
        verbose_name="Dia da semana"
    )

    horario_inicio = models.TimeField(
        verbose_name="Horário inicial"
    )

    horario_fim = models.TimeField(
        verbose_name="Horário final"
    )

    descricao = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Motivo"
    )

    ativo = models.BooleanField(
        default=True
    )

    criado_em = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        dia = dict(self.DIAS_SEMANA).get(
            self.dia_semana
        )

        return (
            f"{dia} - "
            f"{self.horario_inicio.strftime('%H:%M')} "
            f"às "
            f"{self.horario_fim.strftime('%H:%M')}"
        )

    class Meta:

        ordering = [
            "dia_semana",
            "horario_inicio",
        ]

        verbose_name = "Bloqueio Semanal"

        verbose_name_plural = "Bloqueios Semanais"


class Agendamento(models.Model):

    STATUS_CHOICES = [
        ("PENDENTE", "Pendente"),
        ("CONFIRMADO", "Confirmado"),
        ("FINALIZADO", "Finalizado"),
        ("CANCELADO", "Cancelado"),
    ]

    nome = models.CharField(
        max_length=100
    )

    telefone = models.CharField(
        max_length=20
    )

    servico = models.ForeignKey(
        Servico,
        on_delete=models.CASCADE
    )

    data = models.DateField()

    horario = models.TimeField()

    valor = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDENTE"
    )

    criado_em = models.DateTimeField(
        auto_now_add=True
    )

    atualizado_em = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        ordering = [
            "data",
            "horario",
        ]

        indexes = [
            models.Index(fields=["data"]),
            models.Index(fields=["status"]),
        ]

        constraints = [
            models.UniqueConstraint(
                fields=["data", "horario"],
                name="horario_unico"
            )
        ]

        verbose_name = "Agendamento"

        verbose_name_plural = "Agendamentos"

    def save(self, *args, **kwargs):

        if self.servico_id:
            self.valor = self.servico.preco

        super().save(*args, **kwargs)

    def __str__(self):

        return (
            f"{self.nome} - "
            f"{self.servico.nome} - "
            f"{self.data} {self.horario}"
        )