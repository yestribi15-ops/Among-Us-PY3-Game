import socket
import threading
import json
import random
import string

SERVER_IP = "0.0.0.0"
PORT = 5555

# Generar código de sala de 6 letras
CODIGO_SALA = "".join(random.choices(string.ascii_uppercase, k=6))

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER_IP, PORT))
server.listen()
print(f"[CREADOR] Servidor de Among Us iniciado.")
print(f"[SALA] Código de la partida: {CODIGO_SALA} 🚀")

game_state = {}

def manejar_cliente(conn, jugador_id):
    global game_state
    try:
        # Validar código de 6 letras
        codigo_recibido = conn.recv(1024).decode().strip().upper()
        if codigo_recibido != CODIGO_SALA:
            conn.send("ERROR: Código incorrecto.".encode())
            conn.close()
            return
        
        conn.send(f"OK:{jugador_id}".encode())
        # Registro inicial en la nave
        game_state[jugador_id] = {"x": 400, "y": 300, "rol": "Tripulante", "vivo": True}
    except:
        conn.close()
        return

    # Bucle de actualización
    while True:
        try:
            data = conn.recv(1024).decode()
            if not data: 
                break
            if data == "get_state":
                conn.send(json.dumps(game_state).encode())
            else:
                # Recibe movimientos del Client_Bot y actualiza el servidor
                game_state[jugador_id] = json.loads(data)
                conn.send(json.dumps(game_state).encode())
        except:
            break

    print(f"[CREADOR] Astronauta #{jugador_id} abandonó la partida.")
    if jugador_id in game_state: 
        del game_state[jugador_id]
    conn.close()

id_actual = 0
while True:
    conn, addr = server.accept()
    threading.Thread(target=manejar_cliente, args=(conn, id_actual)).start()
    id_actual += 1
