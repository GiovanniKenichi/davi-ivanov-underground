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