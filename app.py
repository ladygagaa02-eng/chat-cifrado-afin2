from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import math

app = Flask(__name__)
socketio = SocketIO(app)

ALFABETO = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
MOD = len(ALFABETO)

# -------------------------------
# Matemática: Euclides Extendido
# -------------------------------
def euclides_extendido(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = euclides_extendido(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def inverso_multiplicativo(a):
    gcd, x, _ = euclides_extendido(a, MOD)
    return x % MOD

# -------------------------------
# Cifrado Afín
# -------------------------------
def cifrar(mensaje, a, b):
    resultado = ""
    mensaje = mensaje.upper()

    for letra in mensaje:
        if letra in ALFABETO:
            p = ALFABETO.index(letra)
            c = (a * p + b) % MOD
            resultado += ALFABETO[c]
        else:
            resultado += letra

    return resultado

def descifrar(mensaje, a, b):
    a_inv = inverso_multiplicativo(a)
    resultado = ""

    for letra in mensaje:
        if letra in ALFABETO:
            c = ALFABETO.index(letra)
            p = (a_inv * (c - b)) % MOD
            resultado += ALFABETO[p]
        else:
            resultado += letra

    return resultado

# -------------------------------
# Rutas
# -------------------------------
@app.route("/")
def index():
    return render_template("index.html")

# -------------------------------
# WebSocket
# -------------------------------
@socketio.on("mensaje")
def manejar_mensaje(data):
    mensaje = data["mensaje"]
    a = int(data["a"])
    b = int(data["b"])

    cifrado = cifrar(mensaje, a, b)
    descifrado = descifrar(cifrado, a, b)

    emit("respuesta", {
        "original": mensaje,
        "cifrado": cifrado,
        "descifrado": descifrado
    }, broadcast=True)

if __name__ == "__main__":
    socketio.run(app, debug=True)
