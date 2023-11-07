import cv2
from pyzbar.pyzbar import decode 
from twilio.rest import Client
import time
import sqlite3

#Author: Armenta Alvarez Aneth
#Author: López Manuel José Luis
sid = 'SID'
token = 'TOKEN'
cliente = Client(sid, token) # Crea una instancia del cliente de Twilio
codigos_escaneados = set()# Utiliza un conjunto para almacenar los códigos QR escaneados
codigos_escaneados_lista = [] # Lista para almacenar los códigos escaneados

conexion = sqlite3.connect('escaneos_codigo.db')
cursor = conexion.cursor()

cursor.execute('''                        
    CREATE TABLE IF NOT EXISTS escaneos (
        fecha TEXT,
        numero TEXT
    )
''') 
conexion.commit()

def guardar_BD(fecha, numero):
    cursor.execute('INSERT INTO escaneos (fecha, numero) VALUES (?, ?)', (fecha, numero))
    conexion.commit()

def send(destinatario, mensaje):
    mensaje_enviado = cliente.messages.create(
        body=mensaje,
        from_='+12563630491',  #Número de teléfono de Twilio
        to=destinatario
    )

    print(f'Mensaje enviado a {destinatario}: {mensaje_enviado.sid}')

def leer_qr_y_enviar_mensaje():
    cap = cv2.VideoCapture('http://IP del celular:Puerto/video')    # Abre la cámara de DroidCam
    while True:
        ret, frame = cap.read()        # Lee un cuadro de la cámara
        decoded_objects = decode(frame)
           # Decodifica códigos QR en el cuadro
        for obj in decoded_objects:
            codigo_qr = obj.data.decode('utf-8') # Obtiene el contenido del código QR

            # Si el código QR no ha sido escaneado previamente, envía un mensaje y registra el código en la base de datos
            if codigo_qr not in codigos_escaneados:
                codigos_escaneados.add(codigo_qr)
                codigos_escaneados_lista.append(codigo_qr)
                hora_actual = time.strftime("%Y-%m-%d %H:%M:%S") 
                mensaje = f'El alumno ha ingresado a la Universidad ({hora_actual})'
                send(codigo_qr, mensaje)
                print(f'Código QR escaneado: {codigo_qr}')
                guardar_BD(hora_actual, codigo_qr)

        cv2.imshow("QR Code Scanner", frame)   
        if cv2.waitKey(1) & 0xFF == ord('q'):    
            break
    cap.release() 
    cv2.destroyAllWindows()

if __name__ == '__main__':
    leer_qr_y_enviar_mensaje()
    # Después de salir del bucle, imprime los códigos QR escaneados y cierra la conexión a la base de datos
    print("Códigos QR escaneados:")
    for codigo in codigos_escaneados_lista:
        print(codigo)
    conexion.close()