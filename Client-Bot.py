import socket
import json

class ClienteConector:
    def __init__(self, ip="127.0.0.1", puerto=5555):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip = ip
        self.puerto = puerto
        self.my_id = None

    def conectar(self, codigo_sala):
        try:
            self.client.connect((self.ip, self.puerto))
            
            # Enviar el código de 6 letras al servidor
            self.client.send(codigo_sala.encode())
            
            # Recibir la respuesta de validación
            respuesta = self.client.recv(1024).decode()
            
            if respuesta.startswith("OK:"):
                self.my_id = respuesta.split(":")[1]
                print(f"[CONECTOR] ¡Código correcto! Entrando a la sala. Mi ID es: {self.my_id}")
                return True
            else:
                print(f"[CONECTOR] Rechazado: {respuesta}")
                self.client.close()
                return False
        except Exception as e:
            print(f"[CONECTOR] Error al conectar: {e}")
            return False

    def actualizar_y_recibir(self, mis_datos):
        try:
            self.client.send(json.dumps(mis_datos).encode())
            respuesta = self.client.recv(1024).decode()
            return json.loads(respuesta)
        except:
            return {}
