from datetime import datetime, timedelta


def gerar_horarios():

    inicio = datetime.strptime("09:00", "%H:%M")
    fim = datetime.strptime("19:00", "%H:%M")

    horarios = []

    while inicio < fim:

        horarios.append(
            inicio.strftime("%H:%M")
        )

        inicio += timedelta(minutes=30)

    return horarios