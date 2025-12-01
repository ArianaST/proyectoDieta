from typing import Dict, Any, List
import copy

# ------------------------------------------------------------
#   Catálogo platillos
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
    desayunos: List[Platillo] = [
        # --- ORIGINALES (4) ---
        {"tipo": "desayuno", "nombre": "Avena con leche y plátano",         "calorias": 350.0, "proteina": 14.0, "lipidos": 38.0, "carbohidratos": 158.0, "costo": 15.0},
        {"tipo": "desayuno", "nombre": "Huevos con frijoles y tortilla",    "calorias": 420.0, "proteina": 22.0, "lipidos": 38.0, "carbohidratos": 158.0, "costo": 15.0},
        {"tipo": "desayuno", "nombre": "Yogur con fruta y granola",         "calorias": 320.0, "proteina": 12.0, "lipidos": 38.0, "carbohidratos": 158.0, "costo": 15.0},
        {"tipo": "desayuno", "nombre": "Molletes de frijol con queso",      "calorias": 450.0, "proteina": 18.0, "lipidos": 38.0, "carbohidratos": 158.0, "costo": 15.0},

        # --- NUEVOS (30) (Precios restaurados a la referencia del usuario) ---
        {"tipo": "desayuno", "nombre": "Huevo a la mexicana con 2 tortillas y papaya", "calorias": 348.0, "proteina": 15.6, "lipidos": 12.4, "carbohidratos": 43.9, "costo": 75.0},
        {"tipo": "desayuno", "nombre": "Huevo con ejotes, 2 tortillas y melón",        "calorias": 356.0, "proteina": 15.8, "lipidos": 12.9, "carbohidratos": 45.0, "costo": 75.0},
        {"tipo": "desayuno", "nombre": "Huevo con salsa roja, 2 tortillas y manzana",  "calorias": 348.0, "proteina": 15.0, "lipidos": 12.5, "carbohidratos": 44.9, "costo": 75.0},
        {"tipo": "desayuno", "nombre": "Huevo con verdura, 2 tortillas y pera",        "calorias": 354.0, "proteina": 16.3, "lipidos": 12.6, "carbohidratos": 44.8, "costo": 75.0},
        {"tipo": "desayuno", "nombre": "Huevo con queso panela y 1 bolillo",           "calorias": 370.5, "proteina": 21.5, "lipidos": 13.8, "carbohidratos": 38.4, "costo": 82.0},
        {"tipo": "desayuno", "nombre": "Huevo con chorizo y 2 tortillas",              "calorias": 364.2, "proteina": 18.5, "lipidos": 19.7, "carbohidratos": 27.2, "costo": 90.0},
        {"tipo": "desayuno", "nombre": "Huevo con jamón, 2 tortillas y fruta",         "calorias": 395.0, "proteina": 19.0, "lipidos": 19.7, "carbohidratos": 42.0, "costo": 90.0},
        {"tipo": "desayuno", "nombre": "Huevo con tocino y 2 tortillas",               "calorias": 364.2, "proteina": 18.5, "lipidos": 19.7, "carbohidratos": 27.2, "costo": 90.0},
        {"tipo": "desayuno", "nombre": "Huevo con salchicha, 2 tortillas y té",        "calorias": 364.2, "proteina": 18.5, "lipidos": 19.7, "carbohidratos": 27.2, "costo": 82.0},
        {"tipo": "desayuno", "nombre": "Huevo con frijoles y pan tostado (2)",         "calorias": 376.2, "proteina": 20.5, "lipidos": 14.0, "carbohidratos": 43.0, "costo": 72.0},
        {"tipo": "desayuno", "nombre": "Huevo revuelto con jamón y pan tostado",       "calorias": 350.0, "proteina": 19.0, "lipidos": 15.0, "carbohidratos": 30.0, "costo": 75.0},
        {"tipo": "desayuno", "nombre": "Huevo ranchero (2 pzas) con fruta",            "calorias": 383.2, "proteina": 14.5, "lipidos": 18.9, "carbohidratos": 38.7, "costo": 88.0},
        {"tipo": "desayuno", "nombre": "Huevo revuelto con tortilla (Migas) y fruta",  "calorias": 383.2, "proteina": 14.5, "lipidos": 18.9, "carbohidratos": 38.7, "costo": 78.0},
        {"tipo": "desayuno", "nombre": "Tortilla española con ensalada y pan",         "calorias": 360.0, "proteina": 15.0, "lipidos": 19.0, "carbohidratos": 30.0, "costo": 75.0},
        {"tipo": "desayuno", "nombre": "Cereal con leche, plátano y almendras",        "calorias": 456.0, "proteina": 19.2, "lipidos": 18.6, "carbohidratos": 56.0, "costo": 60.0},
        {"tipo": "desayuno", "nombre": "Hot cakes (2) con leche y fresas",             "calorias": 458.0, "proteina": 14.0, "lipidos": 15.5, "carbohidratos": 72.7, "costo": 67.5},
        {"tipo": "desayuno", "nombre": "Pan francés con durazno y leche",              "calorias": 465.0, "proteina": 14.0, "lipidos": 15.2, "carbohidratos": 74.6, "costo": 67.5},
        {"tipo": "desayuno", "nombre": "Licuado de frutas con cereal y amaranto",      "calorias": 436.0, "proteina": 18.7, "lipidos": 13.3, "carbohidratos": 74.6, "costo": 52.5},
        {"tipo": "desayuno", "nombre": "Tamal de dulce y vaso de leche",               "calorias": 495.0, "proteina": 12.0, "lipidos": 15.0, "carbohidratos": 72.0, "costo": 33.0},
        {"tipo": "desayuno", "nombre": "Pan dulce, vaso de leche y manzana",           "calorias": 447.5, "proteina": 11.0, "lipidos": 12.0, "carbohidratos": 78.0, "costo": 45.0},
        {"tipo": "desayuno", "nombre": "Atole con leche y 1 pan tostado con mermelada","calorias": 380.0, "proteina": 10.0, "lipidos": 7.0,  "carbohidratos": 68.0, "costo": 37.5},
        {"tipo": "desayuno", "nombre": "Licuado de plátano con avena y nuez",          "calorias": 395.0, "proteina": 15.0, "lipidos": 15.0, "carbohidratos": 58.0, "costo": 45.0},
        {"tipo": "desayuno", "nombre": "Yogur griego con granola y frutos rojos",      "calorias": 340.0, "proteina": 18.0, "lipidos": 8.0,  "carbohidratos": 45.0, "costo": 52.5},
        {"tipo": "desayuno", "nombre": "Chilaquiles rojos con pollo y frijoles",       "calorias": 540.0, "proteina": 28.0, "lipidos": 22.0, "carbohidratos": 55.0, "costo": 112.5},
        {"tipo": "desayuno", "nombre": "Enchiladas de pollo (2) con crema",            "calorias": 450.0, "proteina": 23.0, "lipidos": 20.0, "carbohidratos": 40.0, "costo": 112.5},
        {"tipo": "desayuno", "nombre": "Enfrijoladas (3) con queso y lechuga",        "calorias": 570.0, "proteina": 28.5, "lipidos": 16.5, "carbohidratos": 75.0, "costo": 97.5},
        {"tipo": "desayuno", "nombre": "Molletes (2) con pico de gallo",               "calorias": 589.0, "proteina": 29.5, "lipidos": 16.7, "carbohidratos": 79.2, "costo": 82.5},
        {"tipo": "desayuno", "nombre": "Tacos de huevo (2) y fruta picada",            "calorias": 380.0, "proteina": 16.0, "lipidos": 14.0, "carbohidratos": 45.0, "costo": 75.0},
        {"tipo": "desayuno", "nombre": "Sándwich de jamón y queso con fruta",          "calorias": 420.0, "proteina": 20.0, "lipidos": 15.0, "carbohidratos": 50.0, "costo": 60.0},
        {"tipo": "desayuno", "nombre": "Quesadillas (2) con aguacate y salsa",         "calorias": 390.0, "proteina": 18.0, "lipidos": 18.0, "carbohidratos": 35.0, "costo": 60.0},
    ]

    comidas: List[Platillo] = [
        # --- ORIGINALES (4) ---
        {"tipo": "comida", "nombre": "Pollo asado con arroz y ensalada",      "calorias": 680.0, "proteina": 36.0, "lipidos": 45.0, "carbohidratos": 180.0, "costo": 30.0},
        {"tipo": "comida", "nombre": "Pescado al horno con verduras",         "calorias": 600.0, "proteina": 32.0, "lipidos": 45.0, "carbohidratos": 180.0, "costo": 30.0},
        {"tipo": "comida", "nombre": "Tacos de lentejas con arroz",           "calorias": 620.0, "proteina": 26.0, "lipidos": 45.0, "carbohidratos": 180.0, "costo": 30.0},
        {"tipo": "comida", "nombre": "Guiso de res con papa y zanahoria",     "calorias": 720.0, "proteina": 40.0, "lipidos": 45.0, "carbohidratos": 180.0, "costo": 30.0},

        # --- NUEVOS (30) ---
        {"tipo": "comida", "nombre": "Menú: Consomé, Pechuga asada y Arroz",           "calorias": 530.0, "proteina": 35.0, "lipidos": 15.0, "carbohidratos": 60.0, "costo": 95.0},
        {"tipo": "comida", "nombre": "Menú: Sopa verduras, Filete pescado y Ensalada", "calorias": 510.0, "proteina": 38.0, "lipidos": 14.0, "carbohidratos": 55.0, "costo": 105.0},
        {"tipo": "comida", "nombre": "Menú: Sopa hongos, Bistec asado y Frijoles",     "calorias": 580.0, "proteina": 35.0, "lipidos": 20.0, "carbohidratos": 65.0, "costo": 110.0},
        {"tipo": "comida", "nombre": "Crema de brócoli con Pollo a la plancha",        "calorias": 550.0, "proteina": 35.0, "lipidos": 25.0, "carbohidratos": 45.0, "costo": 115.0},
        {"tipo": "comida", "nombre": "Crema de calabacitas con Milanesa de res",       "calorias": 650.0, "proteina": 38.0, "lipidos": 30.0, "carbohidratos": 55.0, "costo": 120.0},
        {"tipo": "comida", "nombre": "Crema de poblano y Pescado empapelado",          "calorias": 540.0, "proteina": 36.0, "lipidos": 22.0, "carbohidratos": 45.0, "costo": 125.0},
        {"tipo": "comida", "nombre": "Sopa de tortilla con Tacos dorados de pollo",    "calorias": 620.0, "proteina": 28.0, "lipidos": 28.0, "carbohidratos": 65.0, "costo": 110.0},
        {"tipo": "comida", "nombre": "Sopa de pasta y Picadillo de res con verduras",  "calorias": 580.0, "proteina": 30.0, "lipidos": 25.0, "carbohidratos": 58.0, "costo": 100.0},
        {"tipo": "comida", "nombre": "Sopa de lentejas y Quesadillas (2)",             "calorias": 550.0, "proteina": 25.0, "lipidos": 22.0, "carbohidratos": 68.0, "costo": 95.0},
        {"tipo": "comida", "nombre": "Sopa de frijol y Ensalada de pollo",             "calorias": 540.0, "proteina": 32.0, "lipidos": 20.0, "carbohidratos": 55.0, "costo": 105.0},
        {"tipo": "comida", "nombre": "Caldo tlalpeño (con arroz y pollo)",             "calorias": 480.0, "proteina": 28.0, "lipidos": 18.0, "carbohidratos": 45.0, "costo": 85.0},
        {"tipo": "comida", "nombre": "Pollo a la plancha, arroz y aguacate",           "calorias": 520.0, "proteina": 35.0, "lipidos": 20.0, "carbohidratos": 50.0, "costo": 125.0},
        {"tipo": "comida", "nombre": "Pescado empapelado con arroz jardinera",         "calorias": 510.0, "proteina": 33.0, "lipidos": 18.0, "carbohidratos": 55.0, "costo": 135.0},
        {"tipo": "comida", "nombre": "Ternera al horno con puré de papa y verduras",   "calorias": 560.0, "proteina": 34.0, "lipidos": 22.0, "carbohidratos": 52.0, "costo": 145.0},
        {"tipo": "comida", "nombre": "Albóndigas de res con frijoles y tortillas",     "calorias": 613.0, "proteina": 38.0, "lipidos": 31.0, "carbohidratos": 48.0, "costo": 120.0},
        {"tipo": "comida", "nombre": "Bistec con salsa morita, arroz y frijoles",      "calorias": 580.0, "proteina": 38.0, "lipidos": 31.0, "carbohidratos": 40.0, "costo": 125.0},
        {"tipo": "comida", "nombre": "Chicharrón en salsa verde, frijoles y tortillas","calorias": 650.0, "proteina": 35.0, "lipidos": 40.0, "carbohidratos": 35.0, "costo": 115.0},
        {"tipo": "comida", "nombre": "Estofado de res con papas y arroz",              "calorias": 590.0, "proteina": 35.0, "lipidos": 32.0, "carbohidratos": 45.0, "costo": 130.0},
        {"tipo": "comida", "nombre": "Pollo en salsa verde con arroz y frijoles",      "calorias": 560.0, "proteina": 35.0, "lipidos": 32.0, "carbohidratos": 48.0, "costo": 120.0},
        {"tipo": "comida", "nombre": "Tinga de res con tostadas (3) y crema",          "calorias": 610.0, "proteina": 32.0, "lipidos": 35.0, "carbohidratos": 45.0, "costo": 120.0},
        {"tipo": "comida", "nombre": "Costillitas de cerdo en guajillo y arroz",       "calorias": 680.0, "proteina": 35.0, "lipidos": 42.0, "carbohidratos": 45.0, "costo": 130.0},
        {"tipo": "comida", "nombre": "Pescado a la veracruzana y arroz blanco",        "calorias": 520.0, "proteina": 33.0, "lipidos": 24.0, "carbohidratos": 48.0, "costo": 135.0},
        {"tipo": "comida", "nombre": "Pollo con mole, arroz rojo y tortillas",         "calorias": 720.0, "proteina": 32.0, "lipidos": 45.0, "carbohidratos": 55.0, "costo": 140.0},
        {"tipo": "comida", "nombre": "Cochinita pibil, cebolla y 3 tortillas",         "calorias": 650.0, "proteina": 30.0, "lipidos": 40.0, "carbohidratos": 45.0, "costo": 130.0},
        {"tipo": "comida", "nombre": "Puntas al albañil con frijoles de olla",         "calorias": 610.0, "proteina": 35.0, "lipidos": 38.0, "carbohidratos": 38.0, "costo": 125.0},
        {"tipo": "comida", "nombre": "Milanesa empanizada con ensalada y arroz",       "calorias": 710.0, "proteina": 36.0, "lipidos": 38.0, "carbohidratos": 58.0, "costo": 135.0},
        {"tipo": "comida", "nombre": "Filete de pescado empanizado, ensalada, arroz",  "calorias": 620.0, "proteina": 35.0, "lipidos": 38.0, "carbohidratos": 45.0, "costo": 130.0},
        {"tipo": "comida", "nombre": "Arroz con pollo al horno y verduras al vapor",   "calorias": 550.0, "proteina": 25.0, "lipidos": 22.0, "carbohidratos": 65.0, "costo": 110.0},
        {"tipo": "comida", "nombre": "Caldo gallego con 2 piezas de pan",              "calorias": 658.0, "proteina": 40.0, "lipidos": 28.0, "carbohidratos": 60.0, "costo": 127.5},
        {"tipo": "comida", "nombre": "Fabada con porción de arroz",                    "calorias": 650.0, "proteina": 38.0, "lipidos": 30.0, "carbohidratos": 65.0, "costo": 145.0},
    ]

    cenas: List[Platillo] = [
        # --- ORIGINALES (4) ---
        {"tipo": "cena", "nombre": "Ensalada de garbanzo con aguacate",    "calorias": 420.0, "proteina": 18.0, "lipidos": 20.0, "carbohidratos": 150.0, "costo": 20.0},
        {"tipo": "cena", "nombre": "Tostadas de tinga de pollo",           "calorias": 500.0, "proteina": 25.0, "lipidos": 20.0, "carbohidratos": 150.0, "costo": 20.0},
        {"tipo": "cena", "nombre": "Omelette de queso y espinaca",         "calorias": 380.0, "proteina": 22.0, "lipidos": 20.0, "carbohidratos": 150.0, "costo": 20.0},
        {"tipo": "cena", "nombre": "Sopa de verduras con pollo",            "calorias": 390.0, "proteina": 20.0, "lipidos": 20.0, "carbohidratos": 150.0, "costo": 20.0},

        # --- NUEVOS (30) ---
        {"tipo": "cena", "nombre": "Ensalada de atún con galletas saladas y aguacate",  "calorias": 510.0, "proteina": 25.0, "lipidos": 28.0, "carbohidratos": 40.0, "costo": 90.0},
        {"tipo": "cena", "nombre": "Ensalada de pollo con crutones y aderezo",          "calorias": 520.0, "proteina": 30.0, "lipidos": 25.0, "carbohidratos": 35.0, "costo": 97.5},
        {"tipo": "cena", "nombre": "Ensalada del chef con jamón, queso y aderezo",      "calorias": 550.0, "proteina": 28.0, "lipidos": 35.0, "carbohidratos": 20.0, "costo": 105.0},
        {"tipo": "cena", "nombre": "Ensalada de queso de cabra, nuez y pan",            "calorias": 530.0, "proteina": 18.0, "lipidos": 32.0, "carbohidratos": 40.0, "costo": 105.0},
        {"tipo": "cena", "nombre": "Ensalada de espinaca, toronja y pollo a la plancha","calorias": 500.0, "proteina": 30.0, "lipidos": 20.0, "carbohidratos": 45.0, "costo": 82.5},
        {"tipo": "cena", "nombre": "Verduras gratinadas con pechuga de pollo",          "calorias": 510.0, "proteina": 35.0, "lipidos": 25.0, "carbohidratos": 30.0, "costo": 95.0},
        {"tipo": "cena", "nombre": "Tacos al pastor (4 pzas) con piña",                 "calorias": 580.0, "proteina": 28.0, "lipidos": 26.0, "carbohidratos": 58.0, "costo": 75.0},
        {"tipo": "cena", "nombre": "Tacos de barbacoa (3 pzas) con consome",            "calorias": 600.0, "proteina": 30.0, "lipidos": 30.0, "carbohidratos": 50.0, "costo": 82.5},
        {"tipo": "cena", "nombre": "Tacos de carnitas (3 pzas) con salsa",              "calorias": 590.0, "proteina": 30.0, "lipidos": 32.0, "carbohidratos": 45.0, "costo": 75.0},
        {"tipo": "cena", "nombre": "Tacos de canasta (4 pzas) con ensalada de nopal",   "calorias": 560.0, "proteina": 16.0, "lipidos": 28.0, "carbohidratos": 60.0, "costo": 52.5},
        {"tipo": "cena", "nombre": "Tacos de guisado (3 pzas) arroz y huevo",           "calorias": 580.0, "proteina": 22.0, "lipidos": 25.0, "carbohidratos": 65.0, "costo": 67.5},
        {"tipo": "cena", "nombre": "Tacos de frijol (4 pzas) con queso",                "calorias": 550.0, "proteina": 20.0, "lipidos": 18.0, "carbohidratos": 75.0, "costo": 60.0},
        {"tipo": "cena", "nombre": "Tostadas de tinga (3 pzas) con crema",              "calorias": 580.0, "proteina": 25.0, "lipidos": 28.0, "carbohidratos": 55.0, "costo": 75.0},
        {"tipo": "cena", "nombre": "Tostadas de pollo (3 pzas) con aguacate",           "calorias": 560.0, "proteina": 28.0, "lipidos": 25.0, "carbohidratos": 50.0, "costo": 75.0},
        {"tipo": "cena", "nombre": "Sopes con chorizo (3 pzas) y frijoles",             "calorias": 590.0, "proteina": 22.0, "lipidos": 30.0, "carbohidratos": 58.0, "costo": 67.5},
        {"tipo": "cena", "nombre": "Quesadillas surtidas (3 pzas) fritas",              "calorias": 600.0, "proteina": 20.0, "lipidos": 35.0, "carbohidratos": 50.0, "costo": 60.0},
        {"tipo": "cena", "nombre": "Sincronizadas (2 pzas) con pico de gallo",          "calorias": 520.0, "proteina": 25.0, "lipidos": 24.0, "carbohidratos": 48.0, "costo": 67.5},
        {"tipo": "cena", "nombre": "Huarache de carne con queso",                       "calorias": 580.0, "proteina": 30.0, "lipidos": 28.0, "carbohidratos": 55.0, "costo": 82.5},
        {"tipo": "cena", "nombre": "Gorditas de requesón (3 pzas)",                     "calorias": 540.0, "proteina": 24.0, "lipidos": 22.0, "carbohidratos": 60.0, "costo": 60.0},
        {"tipo": "cena", "nombre": "Gorditas de chicharrón (3 pzas)",                   "calorias": 580.0, "proteina": 26.0, "lipidos": 30.0, "carbohidratos": 50.0, "costo": 60.0},
        {"tipo": "cena", "nombre": "Flautas de pollo (4 pzas) con crema y queso",       "calorias": 590.0, "proteina": 28.0, "lipidos": 30.0, "carbohidratos": 52.0, "costo": 75.0},
        {"tipo": "cena", "nombre": "Burritas de carne (2 pzas)",                        "calorias": 560.0, "proteina": 30.0, "lipidos": 22.0, "carbohidratos": 58.0, "costo": 75.0},
        {"tipo": "cena", "nombre": "Hamburguesa con queso y papas",                     "calorias": 600.0, "proteina": 25.0, "lipidos": 30.0, "carbohidratos": 55.0, "costo": 90.0},
        {"tipo": "cena", "nombre": "Hot dog (2 pzas) con jitomate y cebolla",           "calorias": 520.0, "proteina": 18.0, "lipidos": 28.0, "carbohidratos": 48.0, "costo": 45.0},
        {"tipo": "cena", "nombre": "Pizza (2 rebanadas) y ensalada verde",              "calorias": 580.0, "proteina": 24.0, "lipidos": 25.0, "carbohidratos": 65.0, "costo": 60.0},
        {"tipo": "cena", "nombre": "Torta de jamón con aguacate y queso",               "calorias": 550.0, "proteina": 25.0, "lipidos": 22.0, "carbohidratos": 60.0, "costo": 67.5},
        {"tipo": "cena", "nombre": "Tamal salado (1 pza) y atole",                      "calorias": 510.0, "proteina": 12.0, "lipidos": 18.0, "carbohidratos": 75.0, "costo": 33.0},
        {"tipo": "cena", "nombre": "Empanada de atún (3 pzas) y ensalada",              "calorias": 540.0, "proteina": 28.0, "lipidos": 26.0, "carbohidratos": 50.0, "costo": 50.0},
        {"tipo": "cena", "nombre": "Budín azteca (porción grande)",                     "calorias": 560.0, "proteina": 25.0, "lipidos": 28.0, "carbohidratos": 52.0, "costo": 97.5},
        {"tipo": "cena", "nombre": "Lasagna vegetariana y pan de ajo",                  "calorias": 530.0, "proteina": 20.0, "lipidos": 22.0, "carbohidratos": 60.0, "costo": 105.0},
    ]

    return {"desayuno": desayunos, "comida": comidas, "cena": cenas}


def _multiplica_platillo(platillo : Platillo, factor : float, descripcion : str) -> Platillo:
    platillo_x = copy.deepcopy(platillo)
    platillo_x["nombre"] = descripcion + platillo['nombre']
    platillo_x["calorias"] = platillo["calorias"] * factor
    platillo_x["proteina"] = platillo["proteina"] * factor
    platillo_x["carbohidratos"] = platillo["carbohidratos"] * factor
    platillo_x["lipidos"] = platillo["lipidos"] * factor
    platillo_x["costo"] = platillo["costo"] * factor
    return platillo_x


def _extiende_catalogo(catalogo_base: Dict[str, List[Platillo]]) -> Dict[str, List[Platillo]]:
    """
    Función para extender el catálogo base con fracciones y múltiplos de platillos.
    """
    for tipo, platillos in list(catalogo_base.items()):

        nuevos_platillos: List[Platillo] = []
        for platillo in platillos:
            # Fracción 0.3x
            platillo_03x = _multiplica_platillo(platillo, 0.3, "Un tercio de porción de ")
            nuevos_platillos.append(platillo_03x)

            # Fracción 0.5x
            platillo_05x = _multiplica_platillo(platillo, 0.5, "Media porción de ")
            nuevos_platillos.append(platillo_05x)

            # Fracción 0.7x
            platillo_07x = _multiplica_platillo(platillo, 0.7, "Dos tercios de porción de ")
            nuevos_platillos.append(platillo_07x)

            # Múltiplo 1.5x
            platillo_15x = _multiplica_platillo(platillo, 1.5, "Porción y media de ")
            nuevos_platillos.append(platillo_15x)

            # Múltiplo 2x
            platillo_2x = _multiplica_platillo(platillo, 2.0, "Doble porción de ")
            nuevos_platillos.append(platillo_2x)

        catalogo_base[tipo].extend(nuevos_platillos)
    return catalogo_base