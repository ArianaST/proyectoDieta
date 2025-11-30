# app/routes.py
from flask import render_template, request
from pathlib import Path
import pandas as pd

from . import app  # instancia global app
from .core.modelo_csp import resolver_csp
#from .core.recocido import aplicar_recocido aun no ocupo pk es DEMO


# Cargar BD_JUNTA.csv una sola vez
DATA_DIR = app.config.get("DATA_DIR")
if DATA_DIR is None:
    BASE_DIR = Path(__file__).resolve().parent.parent
    DATA_DIR = BASE_DIR / "data"

BD_PATH = DATA_DIR / "BD_JUNTA.csv"

df_bd = pd.read_csv(BD_PATH)
# quitar columnas tipo 'Unnamed: 0' si existen
df_bd = df_bd.loc[:, ~df_bd.columns.str.startswith("Unnamed")]

# endpointtttttttt


@app.route("/", methods=["GET"])
def welcome():
    """
    Pantalla de bienvenida con animación.
    Después de unos segundos redirige al formulario (/inicio).
    """
    return render_template("welcome.html")


@app.route("/inicio", methods=["GET"])
def index():
    """
    Pantalla con el formulario para capturar días, peso, altura y género.
    """
    return render_template("index.html")


@app.route("/loading", methods=["POST"])
def loading():
    """
    Vista intermedia:
      - Recibe datos del formulario.
      - Muestra animación de carga.
      - Reenvía los datos a /plan tras unos segundos.
    """
    dias_raw = request.form.get("dias", "1")
    peso_raw = request.form.get("peso_kg", "0")
    alt_raw = request.form.get("altura_cm", "0")
    edad_raw = request.form.get("edad_anios", "0")

    dias = int(dias_raw) if dias_raw else 1
    peso_kg = float(peso_raw) if peso_raw else 0.0
    altura_cm = float(alt_raw) if alt_raw else 0.0
    genero = request.form.get("genero", "otro")
    edad_anios = int(edad_raw) if edad_raw else 5

    parametros = {
        "dias": dias,
        "peso_kg": peso_kg,
        "altura_cm": altura_cm,
        "genero": genero,
        "edad_anios": edad_anios,
    }

    return render_template("loading.html", parametros=parametros)


@app.route("/plan", methods=["POST"])
def generar_plan():
    """
    Genera el plan DEMO usando el CSP de juguete y muestra los resultados.
    """
    dias_raw = request.form.get("dias", "1")
    peso_raw = request.form.get("peso_kg", "0")
    alt_raw  = request.form.get("altura_cm", "0")
    edad_raw = request.form.get("edad_anios", "5")

    dias = int(dias_raw) if dias_raw else 1
    peso_kg = float(peso_raw) if peso_raw else 0.0
    altura_cm = float(alt_raw) if alt_raw else 0.0
    genero = request.form.get("genero", "otro")
    edad_anios = int(edad_raw) if edad_raw else 5


    parametros = {
        "dias": dias,
        "peso_kg": peso_kg,
        "altura_cm": altura_cm,
        "genero": genero,
        "edad_anios": edad_anios,
    }

    solucion = resolver_csp(parametros, df_bd)
    plan = solucion["plan"]
    resumen = solucion["resumen"]

    return render_template(
        "resultados.html",
        plan=plan,
        resumen=resumen,
        parametros=parametros,
    )
