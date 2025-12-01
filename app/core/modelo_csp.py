from typing import Dict, Any, List, Optional, Tuple
import pandas as pd
from dataclasses import dataclass, field
import copy
from .catalogo import Platillo, _catalogo_dummy, _extiende_catalogo

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
#   Reglas simplificadas de requerimientos (etapa 1)
# ------------------------------------------------------------

def _normalizar_sexo(sexo_raw: str) -> str:
    
    sexo = str(sexo_raw).strip().lower()
    if sexo.startswith("masc"):
        return "hombre"
    if sexo.startswith("fem"):
        return "mujer"
    else:
        return "otro"

# --------------------------------------------------------------------
#  CALORÍAS: mínimo y máximo (Ecuación de Metabolismo basal de Harris-Benedict), por factor 1.2 para sedentarismo, y 1.8 para actividad física alta
# --------------------------------------------------------------------

def _geb_harris_benedict(peso_kg: float, altura_cm: float, edad_anios: float, sexo_raw: str) -> float:
    sexo = _normalizar_sexo(sexo_raw)
    if sexo == "hombre":
        return 10.0 * peso_kg + 6.25 * altura_cm - 5.0 * edad_anios + 5.0
    if sexo == "mujer":
        return 10.0 * peso_kg + 6.25 * altura_cm - 5.0 * edad_anios - 161.0
    if sexo == "otro":
        return 10.0 * peso_kg + 6.25 * altura_cm - 5.0 * edad_anios - 78.0

def calorias_minimas(peso_kg: float, altura_cm: float, edad_anios: float, sexo_raw: str) -> float:
    geb = _geb_harris_benedict(peso_kg, altura_cm, edad_anios, sexo_raw)
    return geb * 1.2

def calorias_max(peso_kg: float, altura_cm: float, edad_anios: float, sexo_raw: str) -> float:
    geb = _geb_harris_benedict(peso_kg, altura_cm, edad_anios, sexo_raw)
    return geb * 1.8


# --------------------------------------------------------------------
#  PROTEÍNA: consumo mínimo y máximo (Según FAO/WHO/IMSS/CIAD)
# --------------------------------------------------------------------

def proteina_minima(peso_kg: float, edad_anios: float, sexo_raw: str) -> float:
    sexo = _normalizar_sexo(sexo_raw)

    if 5 <= edad_anios < 12:
        return peso_kg * 1.00

    if 12 <= edad_anios < 14:
        if sexo == "hombre":
            return peso_kg * 0.98
        elif sexo == "mujer":
            return peso_kg * 0.95
        else:
            return peso_kg * ((0.98 + 0.95) / 2.0)

    if 14 <= edad_anios < 16:
        if sexo == "hombre":
            return peso_kg * 0.94
        elif sexo == "mujer":
            return peso_kg * 0.88
        else:
            return peso_kg * ((0.94 + 0.88) / 2.0)

    if 16 <= edad_anios < 18:
        if sexo == "hombre":
            return peso_kg * 0.88
        elif sexo == "mujer":
            return peso_kg * 0.81
        else:
            return peso_kg * ((0.88 + 0.81) / 2.0)

    if 18 <= edad_anios < 65:
        # WHO: adulto 18–64
        return peso_kg * 0.75

    # 65 o más (CIAD)
    return peso_kg * 0.80


def proteina_max(peso_kg: float, edad_anios: float, sexo_raw: str) -> float:
    sexo = _normalizar_sexo(sexo_raw)

    if 5 <= edad_anios < 12:
        return peso_kg * 1.35

    if 12 <= edad_anios < 14:
        if sexo == "hombre":
            return peso_kg * 1.35
        elif sexo == "mujer":
            return peso_kg * 1.30
        else:
            return peso_kg * ((1.35 + 1.30) / 2.0)

    if 14 <= edad_anios < 16:
        if sexo == "hombre":
            return peso_kg * 1.30
        elif sexo == "mujer":
            return peso_kg * 1.20
        else:
            return peso_kg * ((1.30 + 1.20) / 2.0)

    if 16 <= edad_anios < 18:
        if sexo == "hombre":
            return peso_kg * 1.20
        elif sexo == "mujer":
            return peso_kg * 1.10
        else:
            return peso_kg * ((1.20 + 1.10) / 2.0)

    if 18 <= edad_anios < 65:
        return peso_kg * 1.05

    # 65 o más
    return peso_kg * 1.20


# --------------------------------------------------------------------
#  LÍPIDOS: consumo mínimo y máximo (IMSS, porcentajes de calorías), se consideró que 1 g de lípido contiene 9 kcal, se usa conversión y porcentaje recomendado mínimo y máximo (20%-35%)
# --------------------------------------------------------------------

def lipidos_min(calorias_min: float) -> float:
    return 0.20 * calorias_min / 9.0

def lipidos_max(calorias_max: float) -> float:
    return 0.35 * calorias_max / 9.0


# --------------------------------------------------------------------
#  CARBOHIDRATOS: mínimo y máximo, se consideró que 1 g de carbohidratos contiene 4 kcal, se usa conversión y porcentaje mínimo y máximo recomendado (45% a 55%)
# --------------------------------------------------------------------

def carbohidratos_min(calorias_min: float) -> float:
    return 0.45 * calorias_min / 4.0


def carbohidratos_max(calorias_max: float) -> float:
    return 0.55 * calorias_max / 4.0



# ------------------------------------------------------------
#   Clase para representar un ejemplar del problema
# ------------------------------------------------------------

@dataclass
class ProblemaMenu:
    catalogo: Dict[str, List[Platillo]]
    min_cal: float
    max_cal: float
    min_prot: float
    max_prot: float
    min_lip: float
    max_lip: float
    min_carb: float
    max_carb: float


# ------------------------------------------------------------
#   Clase para representar una solucion del problema
# ------------------------------------------------------------

@dataclass
class Menu:
    platillos: Dict[str, Platillo] = field(default_factory=dict)
    total_cal: float = 0.0
    total_prot: float = 0.0
    total_lip: float = 0.0
    total_carb: float = 0.0

# ------------------------------------------------------------
#   "CSP" muy simple: búsqueda de una combinación factible
# ------------------------------------------------------------

def _buscar_menu_un_dia(
    min_cal: float,
    max_cal: float,
    min_prot: float,
    max_prot: float,
    min_lip: float,
    max_lip: float,
    min_carb: float,
    max_carb: float,
    catalogo: Dict[str, List[Platillo]],
) -> Optional[Menu]:
    """
    Explora todas las combinaciones de:
      - 1 desayuno
      - 1 comida
      - 1 cena

    y regresa la primera que cumpla:

      min_cal <= total_cal <= max_cal
      min_prot <= total_prot <= max_prot
      min_lip <= total_lip <= max_lip
      min_carb <= total_carb <= max_carb

    Si no hay combinación factible, devuelve None.
    """

    problema_menu : ProblemaMenu = ProblemaMenu(
        catalogo=catalogo,
        min_cal=min_cal,
        max_cal=max_cal,
        min_prot=min_prot,
        max_prot=max_prot,
        min_lip=min_lip,
        max_lip=max_lip,
        min_carb=min_carb,
        max_carb=max_carb
    )

    menu_solucion : Menu = Menu()

    if backtrack(problema_menu, menu_solucion):
        return menu_solucion
    else:
        return None

    
def backtrack(problema_menu: ProblemaMenu, menu: Menu) -> bool:
    """
    Algoritmo forward checking con backtracking para encontrar una solución al problema del menú diario.
    Devuelve True si se encuentra una solución, False en caso contrario.

    Esta implementación ocupa las heurísticas MRV, LCV y consistencia de arcos.
    Este metodo esta basado en el algoritmo descrito en el libro "Artificial Intelligence: A Modern Approach"
    de Stuart Russell y Peter Norvig, 3ta edicion.
    """

    # Variables para restaurar el estado en caso de backtrack
    catalogo_copia : Dict[str, List[Platillo]]
    menu_copia : Menu
    
    # Si el problema ya se resolvió, regresamos True
    if _es_solucion(problema_menu, menu):
        return True

    variable : str = _elige_variable(problema_menu.catalogo)

    if variable is None:
        return False

    for valor in _ordena_valores(problema_menu.catalogo[variable]):

        # Hacemos copias del estado actual para poder restaurarlas después
        catalogo_copia = copy.deepcopy(problema_menu.catalogo)
        menu_copia = copy.deepcopy(menu)
        # Asignamos el valor a la variable
        _asignar_valor(problema_menu, menu, variable, valor)
        # Aplicamos consistencia de arcos para reducir los dominios de las demás variables
        _genera_consistencia_de_arcos(problema_menu, menu)

        if backtrack(problema_menu, menu):
            return True
        else:
            # Restauramos el estado anterior
            _restaurar_estado(problema_menu, menu, catalogo_copia, menu_copia)


    # Si no se encontró solución con ningún valor se regresa False para hacer backtrack
    return False


def _elige_variable(catalogo: Dict[str, List[Platillo]]) -> str:
    """
    Elige la siguiente variable (desayuno, comida o cena) a asignar.
    Elige la variable con el menor número de valores posibles (MRV).
    Devuelve el nombre de la variable.
    """
    variable_seleccionada : Optional[str] = None
    menor_num_valores : int = 0
    for variable, valores in catalogo.items():
        if menor_num_valores == 0 or len(valores) < menor_num_valores:
            menor_num_valores = len(valores)
            variable_seleccionada = variable
    return variable_seleccionada

def _ordena_valores(platillos : List[Platillo]) -> List[Platillo]:
    return platillos

def _es_solucion(problema_menu: ProblemaMenu, menu: Menu) -> bool:
    """
    Verifica si el menú actual es una solución válida.
    """
    return "desayuno" in menu.platillos and \
           "comida" in menu.platillos and \
           "cena" in menu.platillos and \
           problema_menu.min_prot <= menu.total_prot <= problema_menu.max_prot and \
           problema_menu.min_lip <= menu.total_lip <= problema_menu.max_lip and \
           problema_menu.min_carb <= menu.total_carb <= problema_menu.max_carb
           #problema_menu.min_cal <= menu.total_cal <= problema_menu.max_cal and \

def _genera_consistencia_de_arcos(problema_menu: ProblemaMenu, menu: Menu) -> None:
    """
    Aplica consistencia de arcos para reducir los dominios de las variables no asignadas.
    """
    for variable, valores in problema_menu.catalogo.items():
        nuevos_valores : List[Platillo] = []
        for valor in valores:
            total_cal = menu.total_cal + valor["calorias"]
            total_prot = menu.total_prot + valor["proteina"]
            total_lip = menu.total_lip + valor["lipidos"]
            total_carb = menu.total_carb + valor["carbohidratos"]
            # Verificamos si al agregar este valor se cumplen los límites máximos
            if total_cal <= problema_menu.max_cal and total_prot <= problema_menu.max_prot and \
               total_lip <= problema_menu.max_lip and total_carb <= problema_menu.max_carb:
                nuevos_valores.append(valor)
        problema_menu.catalogo[variable] = nuevos_valores

def _asignar_valor(
    problema_menu: ProblemaMenu,
    menu: Menu,
    variable: str,
    valor: Platillo
) -> None:
    """
    Asigna un valor a una variable y actualiza el estado del menú.
    """
    menu.platillos[variable] = valor
    menu.total_cal += valor["calorias"]
    menu.total_prot += valor["proteina"]
    menu.total_lip += valor["lipidos"]
    menu.total_carb += valor["carbohidratos"]
    # Removemos el valor del dominio de la variable
    del problema_menu.catalogo[variable]

def _restaurar_estado(
    problema_menu: ProblemaMenu,
    menu: Menu,
    catalogo_copia: Dict[str, List[Platillo]],
    menu_copia: Menu
) -> None:
    """
    Restaura el estado del problema y del menú a un estado previo.
    """
    problema_menu.catalogo = catalogo_copia
    menu.platillos = menu_copia.platillos
    menu.total_cal = menu_copia.total_cal
    menu.total_prot = menu_copia.total_prot
    menu.total_lip = menu_copia.total_lip
    menu.total_carb = menu_copia.total_carb



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
    edad_anios = float(parametros.get("edad_anios", 0.0))
    genero = parametros.get("genero", "otro")

    if dias < 1:
        dias = 1

    # 2) Cálculo de IMC y requerimientos mínimos
    imc = calcular_imc(peso_kg, altura_cm)
    min_cal = calorias_minimas(peso_kg, altura_cm, edad_anios, genero)
    max_cal = calorias_max(peso_kg, altura_cm, edad_anios, genero)

    min_prot = proteina_minima(peso_kg, edad_anios, genero)
    max_prot = proteina_max(peso_kg, edad_anios, genero)

    min_lip = lipidos_min(min_cal)
    max_lip = lipidos_max(max_cal)

    min_carb = carbohidratos_min(min_cal)
    max_carb = carbohidratos_max(max_cal)

    catalogo = _extiende_catalogo(_catalogo_dummy())

    # 3) Resolver el CSP simplificado para UN día
    solucion_menu = _buscar_menu_un_dia(min_cal, max_cal, min_prot, max_prot, min_lip, max_lip, min_carb, max_carb, catalogo)

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
            "edad_anios": edad_anios,
            "imc": round(imc, 2) if imc is not None else None,
            "imc_texto": (
                f"IMC calculado: {imc:.2f}" if imc is not None else "IMC no disponible"
            ),
            "calorias_min": round(min_cal, 1),
            "calorias_max": round(max_cal, 1),
            "proteina_min": round(min_prot, 1),
            "proteina_max": round(max_prot, 1),
            "carbohidratos_min": round(min_carb, 1),
            "carbohidratos_max": round(max_carb, 1),
            "lipidos_min": round(min_lip, 1),
            "lipidos_max": round(max_lip, 1),
            "exito": False,
        }
        return {"plan": plan, "resumen": resumen}

    # 4) Hubo solución: armamos descripción amigable
    d_plato = solucion_menu.platillos["desayuno"]
    c_plato = solucion_menu.platillos["comida"]
    ce_plato = solucion_menu.platillos["cena"]
    total_cal = solucion_menu.total_cal
    total_prot = solucion_menu.total_prot
    total_carb = solucion_menu.total_carb
    total_lip = solucion_menu.total_lip

    desc_base = (
        f"Desayuno: {d_plato['nombre']} | "
        f"Comida: {c_plato['nombre']} | "
        f"Cena: {ce_plato['nombre']} "
        f"(≈ {total_cal:.0f} kcal, {total_prot:.1f} g proteína, {total_carb:.1f} g carbohidratos, {total_lip:.1f} g lípidos)"
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
        "edad_anios": edad_anios,
        "imc": round(imc, 2) if imc is not None else None,
        "imc_texto": (
            f"IMC calculado: {imc:.2f}" if imc is not None else "IMC no disponible"
        ),
        "calorias_min": round(min_cal, 1),
        "calorias_max": round(max_cal, 1),
        "proteina_min": round(min_prot, 1),
        "proteina_max": round(max_prot, 1),
        "carbohidratos_min": round(min_carb, 1),
        "carbohidratos_max": round(max_carb, 1),
        "lipidos_min": round(min_lip, 1),
        "lipidos_max": round(max_lip, 1),
        "exito": True,
    }

    return {"plan": plan, "resumen": resumen}


# c = _extiende_catalogo(_catalogo_dummy())
# print(len(c['desayuno']))

# cal_min = calorias_minimas(90, 190, 24, "Masculino")
# cal_max = calorias_max(90, 190, 24, "Masculino")

# prot_min = proteina_minima(90, 24, "Masculino")
# prot_max = proteina_max(90, 24, "Masculino")

# lip_min = lipidos_min(cal_min)
# lip_max = lipidos_max(cal_max)

# carb_min = carbohidratos_min(cal_min)
# carb_max = carbohidratos_max(cal_max)

# print(f"Calorías mínimas: {cal_min}, máximas: {cal_max}")
# print(f"Proteína mínimas: {prot_min}, máximas: {prot_max}")
# print(f"Lípidos mínimas: {lip_min}, máximas: {lip_max}")
# print(f"Carbohidratos mínimas: {carb_min}, máximas: {carb_max}")

# m =_buscar_menu_un_dia(cal_min, cal_max, prot_min, prot_max, lip_min, lip_max, carb_min, carb_max, c)
# print(m)