import socket
import json
import time
import random

class ClienteConector:
    def __init__(self, ip="127.0.0.1", puerto=5555):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip = ip
        self.puerto = puerto
        self.my_id = None
        self.mis_datos = {"x": 400, "y": 300, "rol": "Tripulante", "vivo": True}

    def conectar(self, codigo_sala):
        try:
            self.client.connect((self.ip, self.puerto))
            self.client.send(codigo_sala.encode())
            respuesta = self.client.recv(1024).decode()
            
            if respuesta.startswith("OK:"):
                self.my_id = respuesta.split(":")[1]
                print(f"[CONECTOR] ¡Código correcto! Entraste con ID: {self.my_id}")
                return True
            else:
                print(f"[CONECTOR] Rechazado por el Creador: {respuesta}")
                self.client.close()
                return False
        except Exception as e:
            print(f"[CONECTOR] Error de conexión: {e}")
            return False

    def simular_movimiento(self):
        print("[SISTEMA] Enviando posiciones de simulación a la nave... (Ctrl+C para salir)")
        try:
            while True:
                # Simular pequeños pasos estilo Among Us
                self.mis_datos["x"] += random.randint(-5, 5)
                self.mis_datos["y"] += random.randint(-5, 5)
                
                # Enviar al servidor y recibir el estado global
                self.client.send(json.dumps(self.mis_datos).encode())
                estado_global = json.loads(self.client.recv(1024).decode())
                
                time.sleep(0.5) # Actualiza cada medio segundo
        except KeyboardInterrupt:
            print("\n[SISTEMA] Desconectando bot.")
            self.client.close()

if __name__ == "__main__":
    conector = ClienteConector()
    codigo = input("Introduce el código de 6 letras de la sala: ")
    if conector.conectar(codigo):
        conector.simular_movimiento()
