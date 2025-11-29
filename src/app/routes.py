# ============================================================
# Politécnica de Santa Rosa
#
# Materia: Arquitecturas de Software
# Profesor: Jesús Salvador López Ortega
# Grupo: ISW28
# Archivo: routes.py
# Descripción: Módulo encargado de definir y registrar las rutas (endpoints)
#              de la aplicación Flask. Actúa como controlador recibiendo las
#              peticiones HTTP (subida, firma, aprobación) y orquestando 
#              la ejecución de los Casos de Uso correspondientes.
# ============================================================
from flask import request, jsonify, render_template, current_app
from src.application.use_cases import UploadBinaryUseCase, SignBinaryUseCase, ApproveBinaryUseCase
from src.infrastructure.file_repository import FileRepository
from src.infrastructure.json_repository import JsonRepository
from src.infrastructure.email_service import EmailService
from src.domain.services import SigningService
from src.domain.models import BinaryFile

def register_routes(app):
    @app.route('/')
    def home():
        return render_template('home.html')

    @app.route('/files', methods=['GET'])
    def list_files():
        return jsonify(JsonRepository().list_records()), 200

    @app.route('/upload', methods=['POST'])
    def upload_binary():
        file = request.files['file']
        environment = request.form.get('environment', 'dev')
        
        # Usamos el correo configurado en main.py como destino
        target_email = app.config['MAIL_USERNAME']

        use_case = UploadBinaryUseCase(
            FileRepository(), 
            JsonRepository(), 
            EmailService()
        )
        
        binary = use_case.execute(file, environment, target_email)
        return jsonify(binary.to_dict())

    @app.route("/sign", methods=["POST"])
    def sign_file():
        data = request.get_json()
        use_case = SignBinaryUseCase(FileRepository(), JsonRepository(), SigningService())
        result = use_case.execute(data.get("file_id"))
        if result: return jsonify(result.to_dict()), 200
        return jsonify({"error": "Error signing"}), 500

    # --- RUTA QUE SE ABRE DESDE EL CORREO ---
    # Archivo: src/app/routes.py (Sección específica de approve_file)

    @app.route('/approve/<file_id>', methods=['GET'])
    def approve_file(file_id):
        sign_use_case = SignBinaryUseCase(FileRepository(), JsonRepository(), SigningService())
        approve_use_case = ApproveBinaryUseCase(sign_use_case)
        
        success = approve_use_case.execute(file_id)
        
        # Estilos CSS incrustados para la página de respuesta
        page_style = """
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background-color: #1c1c1c;
                color: #f0f0f0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            .card {
                background-color: #2a2a2a;
                padding: 40px;
                border-radius: 12px;
                box-shadow: 0 10px 25px rgba(0,0,0,0.5);
                text-align: center;
                max-width: 400px;
                border: 1px solid #444;
            }
            .icon { font-size: 60px; margin-bottom: 20px; }
            h1 { margin: 0 0 15px 0; font-size: 24px; }
            p { color: #aaa; line-height: 1.5; }
            .btn {
                display: inline-block;
                margin-top: 25px;
                padding: 12px 25px;
                background-color: #E63946;
                color: white;
                text-decoration: none;
                border-radius: 6px;
                font-weight: bold;
                transition: background 0.3s;
            }
            .btn:hover { background-color: #C0303E; }
        </style>
        """

        if success:
            return f"""
            <!DOCTYPE html>
            <html lang="es">
            <head>
                <meta charset="UTF-8">
                <title>Aprobación Exitosa</title>
                {page_style}
            </head>
            <body>
                <div class="card">
                    <div class="icon">✅</div>
                    <h1 style="color: #28a745;">¡Operación Exitosa!</h1>
                    <p>El archivo ha sido aprobado y firmado digitalmente de manera correcta.</p>
                    <p>El sistema de producción ya cuenta con la versión verificada.</p>
                    <a href="/" class="btn">Volver al Inicio</a>
                </div>
            </body>
            </html>
            """
        else:
            return f"""
            <!DOCTYPE html>
            <html lang="es">
            <head>
                <meta charset="UTF-8">
                <title>Error de Aprobación</title>
                {page_style}
            </head>
            <body>
                <div class="card" style="border-top: 4px solid #E63946;">
                    <div class="icon">❌</div>
                    <h1 style="color: #E63946;">Error en la Operación</h1>
                    <p>No se pudo aprobar el archivo. Es posible que el enlace haya expirado, el archivo ya esté firmado o no exista.</p>
                    <a href="/" class="btn">Volver al Inicio</a>
                </div>
            </body>
            </html>
            """
    
    @app.route('/clear', methods=['POST'])
    def clear_history():
        try:
            JsonRepository().delete_all()
            FileRepository().delete_all()
            return jsonify({"msg": "ok"}), 200
        except: return jsonify({"error": "err"}), 500