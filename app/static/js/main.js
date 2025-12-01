// app/static/js/main.jsp

document.addEventListener("DOMContentLoaded", () => {
  //  auto-envía el form oculto hacia /plan
  const autoForm = document.getElementById("auto-form");
  if (autoForm) {
    setTimeout(() => {
      autoForm.submit();
    }, 1100);
  }

  //  redirige al formulario (/inicio) tras unos segundos
  const welcomeScreen = document.getElementById("welcome-screen");
  if (welcomeScreen) {
    const nextUrl = welcomeScreen.dataset.nextUrl;
    setTimeout(() => {
      window.location.href = nextUrl;
    }, 2000); // ajusta el tiempo si quieres más/menos
  }
});
