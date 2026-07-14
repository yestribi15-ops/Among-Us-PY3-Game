from flask import Flask, render_template_string, jsonify
import socket
import json

app = Flask(__name__)

def obtener_datos_servidor():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("127.0.0.1", 5555))
        # Enviamos un código falso solo para forzar la respuesta de error del servidor,
        # la cual rompe la conexión pero nos dice si está activo.
        s.send("WEB_CHECK".encode())
        s.close()
        return {"status": "Online"}
    except:
        return {"status": "Offline"}

# Plantilla HTML con espacio para el código de 6 letras
HTML_PANEL = """
<!DOCTYPE html>
<html>
<head>
    <title>Among Us - Panel de Control</title>
    <style>
        body { font-family: sans-serif; background: #11141a; color: white; text-align: center; }
        .contenedor { max-width: 600px; margin: 50px auto; background: #1e2330; padding: 30px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }
        .codigo-box { background: #ffc107; color: #111; font-size: 24px; font-weight: bold; padding: 10px; border-radius: 6px; display: inline-block; letter-spacing: 4px; margin: 15px 0; }
        .jugador { background: #282e3d; padding: 12px; margin: 10px 0; border-radius: 6px; display: flex; justify-content: space-between; align-items: center; }
        .vivo { color: #4caf50; font-weight: bold; }
    </style>
</head>
<body>
    <div class="contenedor">
        <h1>🚀 Sala de Monitoreo - Skeld</h1>
        <p>Pídele al administrador el código de 6 letras que aparece en la consola del Server-Bot para conectar tus Client-Bots.</p>
        
        <!-- Aquí se informaría el estado o acciones del juego remoto -->
        <div id="estado-servidor">Verificando conexión con el Creador...</div>
    </div>

    <script>
        async function verificarServidor() {
            const res = await fetch('/api/estado');
            const datos = await res.json();
            const div = document.getElementById('estado-servidor');
            if (datos.status === "Online") {
                div.innerHTML = '<p style="color: #4caf50;">● El Server-Bot está encendido y esperando jugadores.</p>';
            } else {
                div.innerHTML = '<p style="color: #f44336;">○ El Server-Bot está apagado.</p>';
            }
        }
        setInterval(verificarServidor, 3000);
        verificarServidor();
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_PANEL)

@app.route('/api/estado')
def api_estado():
    return jsonify(obtener_datos_servidor())

if __name__ == '__main__':
    app.run(debug=True, port=5000)
