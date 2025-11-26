# app/__init__.py
from flask import Flask
from pathlib import Path

# instancia global de Flask
app = Flask(__name__)

# Configuración de rutas de archivos
BASE_DIR = Path(__file__).resolve().parent.parent
app.config["BASE_DIR"] = BASE_DIR
app.config["DATA_DIR"] = BASE_DIR / "data"   #jala de esa carpeta la bd


from . import routes 

