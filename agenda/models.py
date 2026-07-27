from django.db import models


from django.db import models

class Servico(models.Model):

    nome = models.CharField(max_length=100)

    descricao = models.TextField(blank=True)

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

    STATUS = (
        ("PENDENTE", "Pendente"),
        ("PAGO", "Pago"),
        ("FINALIZADO", "Finalizado"),
        ("CANCELADO", "Cancelado"),
    )

    nome = models.CharField("Nome", max_length=120)
    telefone = models.CharField("Telefone", max_length=20)

    servico = models.ForeignKey(
        Servico,
        on_delete=models.CASCADE,
        related_name="agendamentos",
        verbose_name="Serviço",
    )

    data = models.DateField("Data")
    horario = models.TimeField("Horário")

    valor = models.DecimalField(
        "Valor",
        max_digits=8,
        decimal_places=2,
        default=0,
    )

    status = models.CharField(
        "Status",
        max_length=20,
        choices=STATUS,
        default="PENDENTE",
    )

    pagamento_id = models.CharField(
        "ID do Pagamento",
        max_length=100,
        blank=True,
        null=True,
    )

    criado_em = models.DateTimeField(
        "Criado em",
        auto_now_add=True,
    )

    class Meta:
        ordering = ["data", "horario"]

        indexes = [
            models.Index(fields=["data"]),
            models.Index(fields=["status"]),
        ]

        constraints = [
            models.UniqueConstraint(
                fields=["data", "horario"],
                name="horario_unico",
            )
        ]

        verbose_name = "Agendamento"
        verbose_name_plural = "Agendamentos"

    def save(self, *args, **kwargs):
        if self.servico_id:
            self.valor = self.servico.preco

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nome} - {self.servico.nome} ({self.data} {self.horario})"