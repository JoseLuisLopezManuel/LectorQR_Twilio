import cv2
#Author: Armenta Alvarez Aneth
#Author: López Manuel José Luis
def decodificar_codigo_qr(direccion):
    imagen = cv2.imread(direccion)
    detector = cv2.QRCodeDetector()
    valor, puntos, rect = detector.detectAndDecode(imagen)
    if valor:
        print(f"Valor del código QR decodificado: {valor}")
    else:
        print("No se encontró un código QR en la imagen.")
if __name__ == "__main__":
    direccion = "codigo_qr_alumno.png"  
    decodificar_codigo_qr(direccion)
