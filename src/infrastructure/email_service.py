# ============================================================
# Politécnica de Santa Rosa
#
# Materia: Arquitecturas de Software
# Profesor: Jesús Salvador López Ortega
# Grupo: ISW28
# Archivo: email_service.py
# Descripción: Implementación del servicio de notificaciones por correo electrónico.
#              Utiliza Flask-Mail para enviar alertas de aprobación cuando un 
#              archivo es subido al entorno de producción, generando enlaces 
#              dinámicos para la firma digital remota.
# ============================================================
# Archivo: src/infrastructure/email_service.py

from flask_mail import Message
from flask import current_app, url_for

class EmailService:
    def send_approval_email(self, recipient_email: str, file_id: str, filename: str):
        try:
            # Genera el enlace de aprobación
            approval_link = url_for('approve_file', file_id=file_id, _external=True)
            
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #e0e0e0; border-radius: 8px; background-color: #f9f9f9; }}
                    .header {{ background-color: #E63946; color: white; padding: 15px; text-align: center; border-radius: 8px 8px 0 0; }}
                    .content {{ padding: 20px; background-color: white; }}
                    .button {{ display: inline-block; padding: 12px 24px; background-color: #28a745; color: white; text-decoration: none; border-radius: 5px; font-weight: bold; margin-top: 20px; }}
                    .footer {{ margin-top: 20px; font-size: 12px; color: #777; text-align: center; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h2>Solicitud de Firma Digital</h2>
                    </div>
                    <div class="content">
                        <p>Hola,</p>
                        <p>Se ha subido un nuevo archivo al entorno de <strong>Producción</strong> que requiere su atención.</p>
                        <table style="width: 100%; margin-bottom: 20px;">
                            <tr>
                                <td style="font-weight: bold;">Archivo:</td>
                                <td>{filename}</td>
                            </tr>
                            <tr>
                                <td style="font-weight: bold;">ID de Referencia:</td>
                                <td>{file_id[:8]}...</td>
                            </tr>
                        </table>
                        <p>Para aprobar este archivo y aplicar la firma digital corporativa, por favor haga clic en el siguiente botón:</p>
                        
                        <div style="text-align: center;">
                            <a href="{approval_link}" class="button">Aprobar y Firmar Documento</a>
                        </div>
                        
                        <p style="margin-top: 30px; font-size: 0.9em;">Si el botón no funciona, copie y pegue el siguiente enlace en su navegador:<br>
                        <a href="{approval_link}">{approval_link}</a></p>
                    </div>
                    <div class="footer">
                        <p>Este es un mensaje automático del Sistema de Firma UPSRJ. Por favor no responda a este correo.</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            msg = Message(
                subject=f"🔔 Acción Requerida: Aprobar {filename}",
                recipients=[recipient_email],
                html=html_content  # Usamos 'html' en lugar de 'body'
            )
            
            current_app.mail.send(msg)
            print(f"✅ Correo enviado a {recipient_email}")
            return True
            
        except Exception as e:
            print(f"❌ Error enviando correo: {e}")
            return False