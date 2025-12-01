// app/static/js/main.js
document.addEventListener("DOMContentLoaded", () => {
  // ==========================
  // 1) Auto-envía el form oculto hacia /plan (loading.html)
  // ==========================
  const autoForm = document.getElementById("auto-form");
  if (autoForm) {
    setTimeout(() => {
      autoForm.submit();
    }, );
  }

  //    (welcome.html -> index)
  const welcomeScreen = document.getElementById("welcome-screen");
  if (welcomeScreen) {
    const nextUrl = welcomeScreen.dataset.nextUrl;
    setTimeout(() => {
      window.location.href = nextUrl;
    }, 2000); // puedes ajustar este tiempo si quieres más/menos bienvenida
  }

  // 3) Navbar: se hace más pequeño al hacer scroll

  const navbar = document.querySelector(".custom-navbar");

  const handleNavbarShrink = () => {
    if (!navbar) return;

    if (window.scrollY > 10) {
      navbar.classList.add("navbar-shrink");
    } else {
      navbar.classList.remove("navbar-shrink");
    }
  };

  handleNavbarShrink();
  window.addEventListener("scroll", handleNavbarShrink);

  // ==========================
  // 4) Animación por filas (renglón por renglón) en tablas de resultados
  // ==========================
  const headings = Array.from(document.querySelectorAll("h1"));
  const isResultadosPage = headings.some((h) =>
    h.textContent.toLowerCase().includes("resultados")
  );

  if (isResultadosPage) {
    // Título principal: entra primero
    const tituloResultados = headings.find((h) =>
      h.textContent.toLowerCase().includes("resultados")
    );
    if (tituloResultados) {
      tituloResultados.classList.add("fade-in-up");
      tituloResultados.style.animationDelay = "0s";
    }

    // Todas las tablas de la página (nutrientes, plan por día, etc.)
    const tablas = document.querySelectorAll("table.table");


    let baseDelay = 0.15;       // empieza un poco después del título
    const rowStep = 0.10;       // MÁS GRANDE = filas más separadas en el tiempo (más lento)
    const gapBetweenTables = 0.15; // pausa al terminar una tabla antes de empezar la siguiente

    tablas.forEach((tabla) => {
      // Fila de encabezado (thead) primero, si existe
      const headerRow = tabla.querySelector("thead tr");
      if (headerRow) {
        headerRow.classList.add("fade-in-up");
        headerRow.style.animationDelay = `${baseDelay}s`;
        baseDelay += rowStep;
      }

      // 👉 Aquí animamos cada fila del cuerpo (tbody) una por una
      const bodyRows = tabla.querySelectorAll("tbody tr");
      bodyRows.forEach((row) => {
        row.classList.add("fade-in-up");

        // Cada fila empieza después de la anterior
        row.style.animationDelay = `${baseDelay}s`;
        baseDelay += rowStep; // controla lo "lento" del desfile de filas
      });

      // Pequeña pausa antes de empezar a animar la siguiente tabla
      baseDelay += gapBetweenTables;
    });

    // Disclaimer / texto de aviso: entra al final de toda la cascada
    const disclaimer = document.querySelector("p.mt-2, p.results-disclaimer");
    if (disclaimer) {
      disclaimer.classList.add("fade-in-up");
      disclaimer.style.animationDelay = `${baseDelay}s`;
    }
  }
});
