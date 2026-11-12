import tkinter as tk
from tkinter import messagebox
import re
import serial
from datetime import datetime


port = 'COM10'
baudrate = 9600

try:
    ser = serial.Serial(port, baudrate, timeout=0.1)
    estado_puerto = "Conectado al puerto serial"
except serial.SerialException:
    ser = None
    estado_puerto = f"Desconectado del puerto "

def textoValido(valor):
    return bool(re.fullmatch(r"[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+", valor))

def fechaValida(valor):
    try:
        datetime.strptime(valor, "%d/%m/%Y")
        return True
    except ValueError:
        return False


def textChangedNombre(valores, indice, modo):
    nombre = varNombre.get().strip()
    if nombre == "":
        tbNombre.config(bg="white")
    elif textoValido(nombre):
        tbNombre.config(bg="lightgreen")
    else:
        tbNombre.config(bg="lightcoral")

def textChangedFecha(valores, indice, modo):
    fecha = varFecha.get().strip()
    if fecha == "":
        tbFecha.config(bg="white")
    elif fechaValida(fecha):
        tbFecha.config(bg="lightgreen")
    else:
        tbFecha.config(bg="lightcoral")

def validar():
    nombre = tbNombre.get().strip()
    fecha = tbFecha.get().strip()

    if not (textoValido(nombre) and fechaValida(fecha)):
        messagebox.showerror(
            "Error",
            "Datos ingresados de manera incorrecta "
            
        )
        return

    messagebox.showinfo(
        "Información",
        f"Datos válidos:\nUsuario: {nombre}\nFecha: {fecha}"
    )

def borrar():
    tbNombre.delete(0, tk.END)
    tbFecha.delete(0, tk.END)
    tbNombre.config(bg="white")
    tbFecha.config(bg="white")

def encender_led():
    if ser:
        ser.write(b'a')
    tbEstadoLed.delete(0, tk.END)
    tbEstadoLed.insert(0, "Encendido")

def apagar_led():
    if ser:
        ser.write(b'b')
    tbEstadoLed.delete(0, tk.END)
    tbEstadoLed.insert(0, "Apagado")

def encender_servo():
    if ser:
        ser.write(b'c')
    tbEstadoServo.delete(0, tk.END)
    tbEstadoServo.insert(0, "Encendido (90°)")

def apagar_servo():
    if ser:
        ser.write(b'd')
    tbEstadoServo.delete(0, tk.END)
    tbEstadoServo.insert(0, "Apagado (0°)")


def leer_serial():
    if ser and ser.in_waiting > 0:
        try:
            linea = ser.readline().decode('utf-8').strip()
            datos = linea.split(',')
            if len(datos) == 3:
                tbRaw.delete(0, tk.END)
                tbRaw.insert(0, datos[0])

                tbCelsius.delete(0, tk.END)
                tbCelsius.insert(0, f"{datos[1]} °C")

                tbFahrenheit.delete(0, tk.END)
                tbFahrenheit.insert(0, f"{datos[2]} °F")
        except Exception:
            pass
    ventana.after(100, leer_serial)

ventana = tk.Tk()
ventana.title("Examen Practico3")

varNombre = tk.StringVar()
varNombre.trace_add("write", textChangedNombre)

varFecha = tk.StringVar()
varFecha.trace_add("write", textChangedFecha)

tk.Label(ventana, text="Nombre:", font=("Segoe UI", 11, "bold")).pack(pady=(10, 0))
tbNombre = tk.Entry(ventana, width=30, justify="center", textvariable=varNombre)
tbNombre.pack(pady=4)

tk.Label(ventana, text="Fecha (DD/MM/AAAA):", font=("Segoe UI", 11, "bold")).pack(pady=(5, 0))
tbFecha = tk.Entry(ventana, width=30, justify="center", textvariable=varFecha)
tbFecha.pack(pady=4)

filaBotonesDatos = tk.Frame(ventana)
filaBotonesDatos.pack(pady=6)
tk.Button(filaBotonesDatos, text="Validar", width=10, command=validar).grid(column=1, row=1, padx=5)
tk.Button(filaBotonesDatos, text="Borrar", width=10, command=borrar).grid(column=2, row=1, padx=5)

lblConexion = tk.Label(ventana, text=estado_puerto, fg="black")
lblConexion.pack(pady=(10, 4))

filaRaw = tk.Frame(ventana)
filaRaw.pack(pady=2)
tk.Label(filaRaw, text="RAWVALUE:", width=12, anchor="e").grid(column=1, row=1, padx=4)
tbRaw = tk.Entry(filaRaw, width=15, justify="center")
tbRaw.grid(column=2, row=1)

filaCelsius = tk.Frame(ventana)
filaCelsius.pack(pady=2)
tk.Label(filaCelsius, text="Celsius:", width=12, anchor="e").grid(column=1, row=1, padx=4)
tbCelsius = tk.Entry(filaCelsius, width=15, justify="center")
tbCelsius.grid(column=2, row=1)

filaFahrenheit = tk.Frame(ventana)
filaFahrenheit.pack(pady=2)
tk.Label(filaFahrenheit, text="Fahrenheit:", width=12, anchor="e").grid(column=1, row=1, padx=4)
tbFahrenheit = tk.Entry(filaFahrenheit, width=15, justify="center")
tbFahrenheit.grid(column=2, row=1)


filaLedEstado = tk.Frame(ventana)
filaLedEstado.pack(pady=(12, 4))
tk.Label(filaLedEstado, text="LED:", width=12, anchor="e").grid(column=1, row=1, padx=4)
tbEstadoLed = tk.Entry(filaLedEstado, width=15, justify="center")
tbEstadoLed.insert(0, "Apagado")
tbEstadoLed.grid(column=2, row=1)

botonesLed = tk.Frame(ventana)
botonesLed.pack(pady=2)
tk.Button(botonesLed, text="Encender LED", width=14, command=encender_led).grid(column=1, row=1, padx=5)
tk.Button(botonesLed, text="Apagar LED", width=14, command=apagar_led).grid(column=2, row=1, padx=5)

filaServoEstado = tk.Frame(ventana)
filaServoEstado.pack(pady=(12, 4))
tk.Label(filaServoEstado, text="Servomotor:", width=12, anchor="e").grid(column=1, row=1, padx=4)
tbEstadoServo = tk.Entry(filaServoEstado, width=15, justify="center")
tbEstadoServo.insert(0, "Apagado (0°)")
tbEstadoServo.grid(column=2, row=1)

botonesServo = tk.Frame(ventana)
botonesServo.pack(pady=(2, 12))
tk.Button(botonesServo, text="Encender Servo", width=14, command=encender_servo).grid(column=1, row=1, padx=5)
tk.Button(botonesServo, text="Apagar Servo", width=14, command=apagar_servo).grid(column=2, row=1, padx=5)

if ser:
    ventana.after(100, leer_serial)

ventana.mainloop()

if ser:
    ser.close()