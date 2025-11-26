# app/csp_dummy.py
from typing import Dict, Any, List
import pandas as pd

def calcular_imc(peso_kg: float, altura_cm: float) -> float | None:
    """
    IMC = peso (kg) / altura^2 (m^2).
    """
    try:
        if peso_kg <= 0 or altura_cm <= 0:
            return None
        altura_m = altura_cm / 100.0
        return peso_kg / (altura_m ** 2)
    except Exception:
        return None


def resolver_csp(parametros: Dict[str, Any], df_bd: pd.DataFrame) -> Dict[str, Any]:
    """
    Versión DEMO simple aqui debe de ir el CSP REAL

    Salida:
      - resumen: con IMC calculado y datos básicos del usuario
      - plan: una fila por día con un texto dummy
    """
    dias = int(parametros.get("dias", 1))
    peso_kg = float(parametros.get("peso_kg", 0.0))
    altura_cm = float(parametros.get("altura_cm", 0.0))
    genero = parametros.get("genero", "otro")

    imc = calcular_imc(peso_kg, altura_cm)

    plan: List[Dict[str, Any]] = []
    for d in range(1, dias + 1):
        plan.append(
            {
                "dia": d,
                "descripcion": f"Menú demo para el día {d} (CSP aún no implementado).",
            }
        )

    resumen: Dict[str, Any] = {
        "mensaje": "CSP DEMO (solo IMC + días, sin restricciones reales)",
        "dias": dias,
        "peso_kg": peso_kg,
        "altura_cm": altura_cm,
        "genero": genero,
        "imc": round(imc, 2) if imc is not None else None,
        "imc_texto": (
            f"IMC calculado: {imc:.2f}" if imc is not None else "IMC no disponible"
        ),
    }

    return {"plan": plan, "resumen": resumen}