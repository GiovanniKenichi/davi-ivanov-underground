document.addEventListener("DOMContentLoaded", () => {

    // ============================
    // ELEMENTOS
    // ============================

    const cards = document.querySelectorAll(".card-servico");

    const servicoInput = document.getElementById("servicoSelecionado");
    const horarioInput = document.getElementById("horarioSelecionado");

    const etapaData = document.getElementById("etapaData");
    const etapaHorario = document.getElementById("etapaHorario");
    const etapaCliente = document.getElementById("etapaCliente");

    const dataInput = document.getElementById("data");
    const horariosContainer = document.querySelector(".horarios");

    const formulario = document.getElementById("formAgendamento");
    const telefone = document.getElementById("telefone");

    // Passos

    const passo2 = document.getElementById("passo2");
    const passo3 = document.getElementById("passo3");
    const passo4 = document.getElementById("passo4");

    // ============================
    // ESCONDE ETAPAS
    // ============================

    etapaData.classList.remove("ativa");
    etapaHorario.classList.remove("ativa");
    etapaCliente.classList.remove("ativa");

    // ============================
    // SERVIÇOS
    // ============================

    cards.forEach(card => {

        card.addEventListener("click", () => {

            cards.forEach(c => c.classList.remove("selecionado"));

            card.classList.add("selecionado");

            servicoInput.value = card.dataset.id;

            etapaData.classList.add("ativa");

            passo2.classList.add("ativo");

            etapaData.scrollIntoView({
                behavior: "smooth",
                block: "center"
            });

        });

    });

    // ============================
    // DATA
    // ============================

    dataInput.addEventListener("change", () => {

        if (!dataInput.value) return;

        etapaHorario.classList.add("ativa");

        passo3.classList.add("ativo");

        carregarHorarios();

    });

    // ============================
    // CARREGA HORÁRIOS
    // ============================

    async function carregarHorarios() {

        horariosContainer.innerHTML = `
            <div class="carregando">
                Carregando horários...
            </div>
        `;

        try {

            const response = await fetch(
                "/agendamento/horarios/?data=" + dataInput.value
            );

            const data = await response.json();

            horariosContainer.innerHTML = "";

            if (data.horarios.length === 0) {

                horariosContainer.innerHTML = `
                    <div class="sem-horarios">
                        😕 Nenhum horário disponível.
                    </div>
                `;

                return;

            }

            data.horarios.forEach(horario => {

                const btn = document.createElement("button");

                btn.type = "button";

                btn.className = "horario-card";

                btn.innerHTML = `
                    <span class="hora">${horario}</span>
                    <small>Disponível</small>
                `;

                btn.addEventListener("click", () => {

                    document
                        .querySelectorAll(".horario-card")
                        .forEach(b => b.classList.remove("selecionado"));

                    btn.classList.add("selecionado");

                    horarioInput.value = horario;

                    etapaCliente.classList.add("ativa");

                    passo4.classList.add("ativo");

                    etapaCliente.scrollIntoView({
                        behavior: "smooth",
                        block: "center"
                    });

                });

                horariosContainer.appendChild(btn);

            });

        }

        catch (erro) {

            console.error(erro);

            horariosContainer.innerHTML = `
                <div class="sem-horarios">
                    Erro ao carregar os horários.
                </div>
            `;

        }

    }

    // ============================
    // MÁSCARA TELEFONE
    // ============================

    if (telefone) {

        telefone.addEventListener("input", function (e) {

            let valor = e.target.value.replace(/\D/g, "");

            valor = valor.replace(/^(\d{2})(\d)/, "($1) $2");

            valor = valor.replace(/(\d{5})(\d)/, "$1-$2");

            e.target.value = valor.substring(0, 15);

        });

    }

    // ============================
    // VALIDAÇÃO
    // ============================

    formulario.addEventListener("submit", function (e) {

        if (servicoInput.value === "") {

            alert("Selecione um serviço.");

            e.preventDefault();

            return;

        }

        if (dataInput.value === "") {

            alert("Selecione uma data.");

            e.preventDefault();

            return;

        }

        if (horarioInput.value === "") {

            alert("Selecione um horário.");

            e.preventDefault();

            return;

        }

    });

});