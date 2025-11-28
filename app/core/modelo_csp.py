from typing import Dict, Any, List, Optional, Tuple
import pandas as pd


# ------------------------------------------------------------
#   Cálculo de IMC
# ------------------------------------------------------------

def calcular_imc(peso_kg: float, altura_cm: float) -> Optional[float]:
    """
    IMC = peso (kg) / altura^2 (m^2).
    Devuelve None si los datos no son válidos.
    """
    try:
        if peso_kg <= 0 or altura_cm <= 0:
            return None
        altura_m = altura_cm / 100.0
        return peso_kg / (altura_m ** 2)
    except Exception:
        return None


# ------------------------------------------------------------
#   Catálogo mínimo de platillos (etapa 1, interno)
# ------------------------------------------------------------

class Platillo(Dict[str, Any]):
    """
    Representación muy simple de un platillo:
      - tipo: 'desayuno' | 'comida' | 'cena'
      - nombre: str
      - calorias: float
      - proteina: float
    Usamos un dict para mantenerlo sencillo y fácil de serializar.
    """
    pass


def _catalogo_dummy() -> Dict[str, List[Platillo]]:
    """
    Catálogo interno de prueba para etapa 1.
    Más adelante se reemplazará / complementará con BD_JUNTA.csv.
    """
    desayunos: List[Platillo] = [
        {"tipo": "desayuno", "nombre": "Avena con leche y plátano",        "calorias": 350.0, "proteina": 14.0},
        {"tipo": "desayuno", "nombre": "Huevos con frijoles y tortilla",   "calorias": 420.0, "proteina": 22.0},
        {"tipo": "desayuno", "nombre": "Yogur con fruta y granola",        "calorias": 320.0, "proteina": 12.0},
        {"tipo": "desayuno", "nombre": "Molletes de frijol con queso",     "calorias": 450.0, "proteina": 18.0},
    ]

    comidas: List[Platillo] = [
        {"tipo": "comida", "nombre": "Pollo asado con arroz y ensalada",   "calorias": 680.0, "proteina": 36.0},
        {"tipo": "comida", "nombre": "Pescado al horno con verduras",      "calorias": 600.0, "proteina": 32.0},
        {"tipo": "comida", "nombre": "Tacos de lentejas con arroz",        "calorias": 620.0, "proteina": 26.0},
        {"tipo": "comida", "nombre": "Guiso de res con papa y zanahoria",  "calorias": 720.0, "proteina": 40.0},
    ]

    cenas: List[Platillo] = [
        {"tipo": "cena", "nombre": "Ensalada de garbanzo con aguacate",    "calorias": 420.0, "proteina": 18.0},
        {"tipo": "cena", "nombre": "Tostadas de tinga de pollo",           "calorias": 500.0, "proteina": 25.0},
        {"tipo": "cena", "nombre": "Omelette de queso y espinaca",         "calorias": 380.0, "proteina": 22.0},
        {"tipo": "cena", "nombre": "Sopa de verduras con pollo",           "calorias": 390.0, "proteina": 20.0},
    ]

    return {"desayuno": desayunos, "comida": comidas, "cena": cenas}


# ------------------------------------------------------------
#   Reglas simplificadas de requerimientos (etapa 1)
# ------------------------------------------------------------

def _calorias_minimas(peso_kg: float, genero: str) -> float:
    """
    Estimación muy simplificada para etapa 1.

    - Si el género empieza con 'M' (Masculino): ~22 kcal/kg.
    - En cualquier otro caso: ~20 kcal/kg.
    """
    sexo = str(genero).strip().lower()
    if sexo.startswith("m"):
        factor = 22.0
    else:
        factor = 20.0
    return max(0.0, peso_kg * factor)


def _proteina_minima(peso_kg: float) -> float:
    """
    Regla estándar simplificada: 0.8 g/kg/día.
    """
    return max(0.0, 0.8 * peso_kg)


# ------------------------------------------------------------
#   "CSP" muy simple: búsqueda de una combinación factible
# ------------------------------------------------------------

def _buscar_menu_un_dia(
    min_cal: float,
    min_prot: float,
    catalogo: Dict[str, List[Platillo]],
) -> Optional[Tuple[Platillo, Platillo, Platillo, float, float]]:
    """
    Explora todas las combinaciones de:
      - 1 desayuno
      - 1 comida
      - 1 cena

    y regresa la primera que cumpla:

      total_cal >= min_cal
      total_prot >= min_prot

    Si no hay combinación factible, devuelve None.
    """
    desayunos = catalogo.get("desayuno", [])
    comidas = catalogo.get("comida", [])
    cenas = catalogo.get("cena", [])

    mejor: Optional[Tuple[Platillo, Platillo, Platillo, float, float]] = None

    for d in desayunos:
        for c in comidas:
            for ce in cenas:
                total_cal = d["calorias"] + c["calorias"] + ce["calorias"]
                total_prot = d["proteina"] + c["proteina"] + ce["proteina"]

                if total_cal >= min_cal and total_prot >= min_prot:
                    # Para etapa 1 basta con la primera combinación factible.
                    mejor = (d, c, ce, total_cal, total_prot)
                    return mejor

    return None


# ------------------------------------------------------------
#   Punto de entrada principal usado por Flask
# ------------------------------------------------------------

def resolver_csp(parametros: Dict[str, Any], df_bd: pd.DataFrame) -> Dict[str, Any]:
    """
    Etapa 1: versión simple del modelo CSP.

    - Calcula IMC y requerimientos mínimos (kcal, proteína).
    - Usa un catálogo interno muy pequeño de platillos mexicanos.
    - Busca una sola combinación factible (desayuno, comida, cena).
    - Genera un plan texto-compatible con resultados.html.

    Nota:
      - El parámetro df_bd se IGNORA por ahora; en versiones posteriores
        se usará BD_JUNTA.csv como base real.
    """
    # 1) Leer parámetros de entrada desde el formulario
    dias = int(parametros.get("dias", 1))
    peso_kg = float(parametros.get("peso_kg", 0.0))
    altura_cm = float(parametros.get("altura_cm", 0.0))
    genero = parametros.get("genero", "otro")

    if dias < 1:
        dias = 1

    # 2) Cálculo de IMC y requerimientos mínimos
    imc = calcular_imc(peso_kg, altura_cm)
    min_cal = _calorias_minimas(peso_kg, genero)
    min_prot = _proteina_minima(peso_kg)

    catalogo = _catalogo_dummy()

    # 3) Resolver el CSP simplificado para UN día
    solucion_menu = _buscar_menu_un_dia(min_cal, min_prot, catalogo)

    plan: List[Dict[str, Any]] = []

    if solucion_menu is None:
        # No se encontró menú que cumpla los mínimos
        mensaje = "No se encontró ningún menú que cumpla los mínimos con el catálogo actual."
        for d in range(1, dias + 1):
            plan.append(
                {
                    "dia": d,
                    "descripcion": mensaje,
                }
            )

        resumen: Dict[str, Any] = {
            "mensaje": mensaje,
            "dias": dias,
            "peso_kg": peso_kg,
            "altura_cm": altura_cm,
            "genero": genero,
            "imc": round(imc, 2) if imc is not None else None,
            "imc_texto": (
                f"IMC calculado: {imc:.2f}" if imc is not None else "IMC no disponible"
            ),
            "calorias_minimas": round(min_cal, 1),
            "proteina_minima": round(min_prot, 1),
            "exito": False,
        }
        return {"plan": plan, "resumen": resumen}

    # 4) Hubo solución: armamos descripción amigable
    d_plato, c_plato, ce_plato, total_cal, total_prot = solucion_menu

    desc_base = (
        f"Desayuno: {d_plato['nombre']} | "
        f"Comida: {c_plato['nombre']} | "
        f"Cena: {ce_plato['nombre']} "
        f"(≈ {total_cal:.0f} kcal, {total_prot:.1f} g proteína)"
    )

    for d in range(1, dias + 1):
        plan.append(
            {
                "dia": d,
                "descripcion": desc_base,
            }
        )

    resumen = {
        "mensaje": "CSP etapa 1: se encontró un menú diario factible.",
        "dias": dias,
        "peso_kg": peso_kg,
        "altura_cm": altura_cm,
        "genero": genero,
        "imc": round(imc, 2) if imc is not None else None,
        "imc_texto": (
            f"IMC calculado: {imc:.2f}" if imc is not None else "IMC no disponible"
        ),
        "calorias_minimas": round(min_cal, 1),
        "proteina_minima": round(min_prot, 1),
        "calorias_menu": round(total_cal, 1),
        "proteina_menu": round(total_prot, 1),
        "exito": True,
    }

    return {"plan": plan, "resumen": resumen}
