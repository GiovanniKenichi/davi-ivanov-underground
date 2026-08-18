// ==========================
// NAVBAR
// ==========================

const navbar = document.querySelector(".navbar");

window.addEventListener("scroll", () => {

    if (window.scrollY > 80) {
        navbar.classList.add("scrolled");
    } else {
        navbar.classList.remove("scrolled");
    }

});

// ==========================
// SCROLL SUAVE
// ==========================

document.querySelectorAll('a[href^="#"]').forEach(link => {

    link.addEventListener("click", function (e) {

        e.preventDefault();

        const target = document.querySelector(this.getAttribute("href"));

        if (target) {

            target.scrollIntoView({

                behavior: "smooth"

            });

        }

    });

});

// ==========================
// ANIMAÇÃO AO ROLAR
// ==========================

const sections = document.querySelectorAll("section");

const reveal = () => {

    const trigger = window.innerHeight * 0.85;

    sections.forEach(section => {

        const top = section.getBoundingClientRect().top;

        if (top < trigger) {

            section.classList.add("show");

        }

    });

};

window.addEventListener("scroll", reveal);

reveal();

// ==========================
// CURSOR
// ==========================

const cursor = document.getElementById("cursor");
const blur = document.getElementById("cursor-blur");

document.addEventListener("mousemove", (e) => {

    cursor.style.left = e.clientX + "px";
    cursor.style.top = e.clientY + "px";

    blur.style.left = e.clientX - 150 + "px";
    blur.style.top = e.clientY - 150 + "px";

});

// ==========================
// HOVER LINKS
// ==========================

document.querySelectorAll("a, button").forEach(item => {

    item.addEventListener("mouseenter", () => {

        cursor.style.transform = "translate(-50%, -50%) scale(2)";

    });

    item.addEventListener("mouseleave", () => {

        cursor.style.transform = "translate(-50%, -50%) scale(1)";

    });

});

// ==========================
// BOTÃO VOLTAR AO TOPO
// ==========================

const topButton = document.createElement("button");

topButton.innerHTML = "↑";

topButton.className = "top-button";

document.body.appendChild(topButton);

window.addEventListener("scroll", () => {

    if (window.scrollY > 500) {

        topButton.classList.add("active");

    } else {

        topButton.classList.remove("active");

    }

});

topButton.onclick = () => {

    window.scrollTo({

        top: 0,

        behavior: "smooth"

    });

};