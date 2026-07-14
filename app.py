from flask import Flask, render_template_string, jsonify
import socket
import json

app = Flask(__name__)

def obtener_datos_servidor():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("127.0.0.1", 5555))
        # Forzar un chequeo de estado saltándonos la verificación de código
        s.send("WEB_CHECK".encode())
        s.close()
        return {"status": "Online"}
    except:
        return {"status": "Offline"}

def obtener_jugadores_reales():
    # Intenta obtener la lista real de juego simulando un cliente get
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("127.0.0.1", 5555))
        s.send("WEB_CHECK".encode()) # Esto desconectará pero sirve para ver si responde
        s.close()
        # Nota: Para un panel dinámico completo, el servidor centraliza los datos. 
        # Enviamos un diccionario de prueba si el Creador responde
        return {"status": "Online"}
    except:
        return {"status": "Offline"}

HTML_PANEL = """
<!DOCTYPE html>
<html>
<head>
    <title>Among Us - Panel de Control</title>
    <style>
        body { font-family: sans-serif; background: #11141a; color: white; text-align: center; padding-top: 50px; }
        .contenedor { max-width: 500px; margin: 0 auto; background: #1e2330; padding: 30px; border-radius: 12px; }
        .status { font-size: 20px; font-weight: bold; padding: 10px; margin: 20px; }
        .online { color: #4caf50; }
        .offline { color: #f44336; }
    </style>
</head>
<body>
    <div class="contenedor">
        <h1>🚀 Sala de Monitoreo - Skeld</h1>
        <p>Estado de los sistemas de red:</p>
        <div id="estado" class="status">Verificando...</div>
    </div>
    <script>
        async function check() {
            const res = await fetch('/api/estado');
            const d = await res.json();
            const div = document.getElementById('estado');
            if(d.status === "Online") {
                div.innerText = "● CREADOR ONLINE (Esperando Conexiones)";
                div.className = "status online";
            } else {
                div.innerText = "○ CREADOR OFFLINE (Enciende Server_Bot.py)";
                div.className = "status offline";
            }
        }
        setInterval(check, 2000); check();
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
