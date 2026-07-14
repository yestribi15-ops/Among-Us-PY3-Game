from flask import Flask, render_template_string, jsonify
import socket
import json

app = Flask(__name__)

def obtener_estado_completo():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("127.0.0.1", 5555))
        
        # Le enviamos el comando especial WEB_CHECK que acepta el servidor
        s.send("WEB_CHECK".encode())
        
        # Inmediatamente después le pedimos el estado global
        s.send("get_state".encode())
        
        # Recibimos el JSON con los jugadores y sus coordenadas
        respuesta = s.recv(4096).decode()
        s.close()
        return json.loads(respuesta)
    except:
        return {}

HTML_PANEL = """
<!DOCTYPE html>
<html>
<head>
    <title>Among Us - Panel de la Nave</title>
    <style>
        body { font-family: sans-serif; background: #11141a; color: white; text-align: center; padding-top: 40px; }
        .contenedor { max-width: 600px; margin: 0 auto; background: #1e2330; padding: 30px; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.3); }
        .jugador-card { background: #282e3d; margin: 10px 0; padding: 15px; border-radius: 8px; display: flex; justify-content: space-between; align-items: center; border-left: 5px solid #ffc107; }
        .coordenadas { color: #00bcd4; font-family: monospace; font-size: 16px; }
        .rol { background: #4caf50; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; }
    </style>
</head>
<body>
    <div class="contenedor">
        <h1>🚀 Radar de la Nave (Skeld)</h1>
        <p>Monitoreo de telemetría de los Client-Bots en tiempo real:</p>
        <div id="lista-jugadores">Buscando señales de trajes espaciales...</div>
    </div>

    <script>
        async function actualizarRadar() {
            try {
                const res = await fetch('/api/estado');
                const jugadores = await res.json();
                const div = document.getElementById('lista-jugadores');
                
                if (Object.keys(jugadores).length === 0) {
                    div.innerHTML = "<p style='color: #f44336;'>○ Creador Offline o sin jugadores en la sala.</p>";
                    return;
                }

                div.innerHTML = "";
                for (const [id, datos] of Object.entries(jugadores)) {
                    div.innerHTML += `
                        <div class="jugador-card">
                            <div>
                                <strong>Astronauta #${id}</strong>
                                <div class="coordenadas">Posición: X:[${datos.x}] Y:[${datos.y}]</div>
                            </div>
                            <span class="rol">${datos.rol}</span>
                        </div>
                    `;
                }
            } catch (e) {
                console.error("Error cargando el radar", e);
            }
        }
        // Solicitar actualizaciones automáticas cada 500 milisegundos (medio segundo)
        setInterval(actualizarRadar, 500);
        actualizarRadar();
    </script>
</body>
</html>
"""

@app.route('/')
def home(): 
    return render_template_string(HTML_PANEL)

@app.route('/api/estado')
def api_estado(): 
    return jsonify(obtener_estado_completo())

if __name__ == '__main__':
    app.run(debug=True, port=5000)
