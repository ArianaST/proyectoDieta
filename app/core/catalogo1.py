from typing import Dict, Any, List
import copy

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
        {"tipo": "desayuno", "nombre": "Avena con leche y plátano",        "calorias": 350.0, "proteina": 14.0, "lipidos": 38.0, "carbohidratos": 158.0, "costo": 15.0},
        {"tipo": "desayuno", "nombre": "Huevos con frijoles y tortilla",   "calorias": 420.0, "proteina": 22.0, "lipidos": 38.0, "carbohidratos": 158.0, "costo": 15.0},
        {"tipo": "desayuno", "nombre": "Yogur con fruta y granola",        "calorias": 320.0, "proteina": 12.0, "lipidos": 38.0, "carbohidratos": 158.0, "costo": 15.0},
        {"tipo": "desayuno", "nombre": "Molletes de frijol con queso",     "calorias": 450.0, "proteina": 18.0, "lipidos": 38.0, "carbohidratos": 158.0, "costo": 15.0},
    ]

    comidas: List[Platillo] = [
        {"tipo": "comida", "nombre": "Pollo asado con arroz y ensalada",   "calorias": 680.0, "proteina": 36.0, "lipidos": 45.0, "carbohidratos": 180.0, "costo": 30.0},
        {"tipo": "comida", "nombre": "Pescado al horno con verduras",      "calorias": 600.0, "proteina": 32.0, "lipidos": 45.0, "carbohidratos": 180.0, "costo": 30.0},
        {"tipo": "comida", "nombre": "Tacos de lentejas con arroz",        "calorias": 620.0, "proteina": 26.0, "lipidos": 45.0, "carbohidratos": 180.0, "costo": 30.0},
        {"tipo": "comida", "nombre": "Guiso de res con papa y zanahoria",  "calorias": 720.0, "proteina": 40.0, "lipidos": 45.0, "carbohidratos": 180.0, "costo": 30.0},
    ]

    cenas: List[Platillo] = [
        {"tipo": "cena", "nombre": "Ensalada de garbanzo con aguacate",    "calorias": 420.0, "proteina": 18.0, "lipidos": 20.0, "carbohidratos": 150.0, "costo": 20.0},
        {"tipo": "cena", "nombre": "Tostadas de tinga de pollo",           "calorias": 500.0, "proteina": 25.0, "lipidos": 20.0, "carbohidratos": 150.0, "costo": 20.0},
        {"tipo": "cena", "nombre": "Omelette de queso y espinaca",         "calorias": 380.0, "proteina": 22.0, "lipidos": 20.0, "carbohidratos": 150.0, "costo": 20.0},
        {"tipo": "cena", "nombre": "Sopa de verduras con pollo",           "calorias": 390.0, "proteina": 20.0, "lipidos": 20.0, "carbohidratos": 150.0, "costo": 20.0},
    ]

    return {"desayuno": desayunos, "comida": comidas, "cena": cenas}


def _extiende_catalogo(catalogo_base: Dict[str, List[Platillo]]) -> Dict[str, List[Platillo]]:
    """
    Función para extender el catálogo base con fracciones y múltiplos de platillos.
    """
    for tipo, platillos in list(catalogo_base.items()):

        nuevos_platillos: List[Platillo] = []
        for platillo in platillos:
            # Fracción 0.3x
            platillo_03x = copy.deepcopy(platillo)
            platillo_03x["nombre"] = f"Un tercio de porción de {platillo['nombre']}"
            platillo_03x["calorias"] = round(platillo["calorias"] * 0.3, 1)
            platillo_03x["proteina"] = round(platillo["proteina"] * 0.3, 1)
            nuevos_platillos.append(platillo_03x)

            # Fracción 0.5x
            platillo_05x = copy.deepcopy(platillo)
            platillo_05x["nombre"] = f"Media porción de {platillo['nombre']}"
            platillo_05x["calorias"] = round(platillo["calorias"] * 0.5, 1)
            platillo_05x["proteina"] = round(platillo["proteina"] * 0.5, 1)
            nuevos_platillos.append(platillo_05x)

            # Fracción 0.7x
            platillo_07x = copy.deepcopy(platillo)
            platillo_07x["nombre"] = f"Dos tercios de porción de {platillo['nombre']}"
            platillo_07x["calorias"] = round(platillo["calorias"] * 0.7, 1)
            platillo_07x["proteina"] = round(platillo["proteina"] * 0.7, 1)
            nuevos_platillos.append(platillo_07x)

            # Múltiplo 1.5x
            platillo_15x = copy.deepcopy(platillo)
            platillo_15x["nombre"] = f"Porción y media de {platillo['nombre']}"
            platillo_15x["calorias"] = round(platillo["calorias"] * 1.5, 1)
            platillo_15x["proteina"] = round(platillo["proteina"] * 1.5, 1)
            nuevos_platillos.append(platillo_15x)

            # Múltiplo 2x
            platillo_2x = copy.deepcopy(platillo)
            platillo_2x["nombre"] = f"Doble porción de {platillo['nombre']}"
            platillo_2x["calorias"] = round(platillo["calorias"] * 2.0, 1)
            platillo_2x["proteina"] = round(platillo["proteina"] * 2.0, 1)
            nuevos_platillos.append(platillo_2x)

        catalogo_base[tipo].extend(nuevos_platillos)
    return catalogo_base