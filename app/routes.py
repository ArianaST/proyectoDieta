# app/routes.py
from flask import render_template, request
from pathlib import Path
import pandas as pd

from . import app  # instancia global app
from .core.modelo_csp import resolver_csp
#from .core.recocido import aplicar_recocido aun no ocupo pk es DEMO

# -------------------------------------------------------------------
# Cargar BD_JUNTA.csv una sola vez
# -------------------------------------------------------------------
DATA_DIR = app.config.get("DATA_DIR")
if DATA_DIR is None:
    BASE_DIR = Path(__file__).resolve().parent.parent
    DATA_DIR = BASE_DIR / "data"

BD_PATH = DATA_DIR / "BD_JUNTA.csv"

df_bd = pd.read_csv(BD_PATH)
# quitar columnas tipo 'Unnamed: 0' si existen
df_bd = df_bd.loc[:, ~df_bd.columns.str.startswith("Unnamed")]

# -------------------------------------------------------------------
# endpointtttttttt
# -------------------------------------------------------------------

@app.route("/", methods=["GET"])
def index():
    # SIEMPRE devolvemos algo
    return render_template("index.html")


@app.route("/plan", methods=["POST"])
def generar_plan():
    # 1) Leer valores del formulario (solo los que usamos)
    dias_raw = request.form.get("dias", "1")
    peso_raw = request.form.get("peso_kg", "0")
    alt_raw  = request.form.get("altura_cm", "0")

    # Manejar campos vacíos ("") para que no truene el cast a int/float
    dias = int(dias_raw) if dias_raw else 1
    peso_kg = float(peso_raw) if peso_raw else 0.0
    altura_cm = float(alt_raw) if alt_raw else 0.0

    genero = request.form.get("genero", "otro")

    # 2) Empaquetar parámetros
    parametros = {
        "dias": dias,
        "peso_kg": peso_kg,
        "altura_cm": altura_cm,
        "genero": genero,
    }

    # 3) Llamar al CSP demo (no usa la BD aún, pero ya tiene la firma lista)
    solucion = resolver_csp(parametros, df_bd)

    plan = solucion["plan"]
    resumen = solucion["resumen"]

    # 4) Renderizar SIEMPRE una respuesta
    return render_template(
        "resultados.html",
        plan=plan,
        resumen=resumen,
        parametros=parametros,
    )