import qrcode
#Author: Armenta Alvarez Aneth
#Author: López Manuel José Luis
def generar_codigo_qr(numero_telefono):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    
    qr.add_data(f"{numero_telefono}")
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save("codigo_qr_alumno.png")

if __name__ == "__main__":
    numero_telefono = "+52"
    generar_codigo_qr(numero_telefono)
    print("Código QR generado y guardado como 'codigo_qr_alumno.png'")