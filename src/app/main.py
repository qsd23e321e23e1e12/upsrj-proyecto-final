# ============================================================
# Politécnica de Santa Rosa
#
# Materia: Arquitecturas de Software
# Profesor: Jesús Salvador López Ortega
# Grupo: ISW28
# Archivo: main.py 
# Descripción: Punto de entrada de la aplicación. Configura e inicializa el 
#              servidor Flask, establece la conexión SMTP para el servicio de 
#              correos y registra las rutas del sistema.
# ============================================================
import sys
import os
from pathlib import Path

# Ajuste de rutas
sys.path.append(str(Path(__file__).parent.parent.parent))

from flask import Flask
from flask_mail import Mail
from src.app.routes import register_routes
from src.common.vars import HOME_HOST

def create_app():
    app = Flask(__name__, template_folder='templates')

    # --- CONFIGURACIÓN DEL CORREO (GMAIL) ---
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    
 
    
    app.config['MAIL_USERNAME'] = 'proyecto3287@gmail.com'  
    app.config['MAIL_PASSWORD'] = 'gkxy knmh fuav xdex' 
    


    app.config['MAIL_DEFAULT_SENDER'] = app.config['MAIL_USERNAME']

    # Inicializar Flask-Mail
    app.mail = Mail(app)

    register_routes(app)
    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=HOME_HOST, debug=True)