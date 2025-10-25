import qrcode

def make_qr_code(data):
    img = qrcode.make(data)
    img.save(f"{data}.png")

make_qr_code("Hello World")
