import sys
import glob
import serial
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
from ttkthemes import ThemedTk

# Función que detecta puertos seriales
def serial_ports():
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')
    
    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

# Inicializar variable de puerto serial
ser = None

# Función para sumar 1 al valor del entry_opcion1 y mostrar el resultado en label_resultado
def sumar_uno(entry, label):
    try:
        valor_actual = int(entry.get())  # Obtener el valor actual del Entry
        nuevo_valor = valor_actual + 1   # Sumar 1
        label.config(text=f"Resultado: {nuevo_valor}")  # Mostrar el resultado en el label
    except ValueError:
        messagebox.showerror("Error", "Por favor ingresa un número válido")

# Conectar al puerto seleccionado
def conectar():
    global ser
    selected_port = combobox_ports.get()
    selected_baud = combobox_baud.get()
    if selected_port and selected_baud:
        try:
            ser = serial.Serial(selected_port, int(selected_baud), timeout=1)
            label_led.config(image=img_led_green)
            messagebox.showinfo("Conexión", "Conectado exitosamente")
        except serial.SerialException as e:
            label_led.config(image=img_led_red)
            messagebox.showerror("Conexión", f"Error al conectar: {e}")
    else:
        messagebox.showerror("Error", "Selecciona un puerto y una velocidad")

# Enviar comando para encender el LED
def led_on():
    if ser:
        try:
            ser.write(b'1')  # Envía el comando '1' para encender el LED
            messagebox.showinfo("LED", "LED encendido")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo enviar el comando: {e}")
    else:
        messagebox.showerror("Error", "No hay conexión serial")

# Enviar comando para apagar el LED
def led_off():
    if ser:
        try:
            ser.write(b'0')  # Envía el comando '0' para apagar el LED
            messagebox.showinfo("LED", "LED apagado")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo enviar el comando: {e}")
    else:
        messagebox.showerror("Error", "No hay conexión serial")

# Configurar PWM para el LED
def configurar_pwm():
    if ser:
        try:
            valor_pwm = int(entry_pwm.get())  # Obtener el valor del entry_pwm
            if 0 <= valor_pwm <= 255:
                ser.write(f'P{valor_pwm}'.encode())  # Envía el valor PWM al ESP32
                messagebox.showinfo("PWM", f"Valor PWM configurado: {valor_pwm}")
            else:
                messagebox.showerror("Error", "Por favor ingresa un valor entre 0 y 255")
        except ValueError:
            messagebox.showerror("Error", "Por favor ingresa un número válido")
    else:
        messagebox.showerror("Error", "No hay conexión serial")

# Función para enviar el valor DAC y mostrar un mensaje de confirmación
def convertir_dac():
    if ser:
        try:
            valor_dac = int(entry_dac.get())  # Obtener el valor del entry_dac
            if 0 <= valor_dac <= 255:
                ser.write(f'D{valor_dac}'.encode())  # Envía el valor DAC al ESP32
                messagebox.showinfo("DAC", f"Valor DAC configurado: {valor_dac}")
            else:
                messagebox.showerror("Error", "Por favor ingresa un valor entre 0 y 255")
        except ValueError:
            messagebox.showerror("Error", "Por favor ingresa un número válido")
    else:
        messagebox.showerror("Error", "No hay conexión serial")

# Función para habilitar/deshabilitar opciones
def deshabilitar_opciones():
    seleccion = spinbox_opcion.get()
    
    # Resetear todo antes de aplicar los cambios
    entry_opcion1.config(state="normal")
    btn_sumar.config(state="normal")
    entry_dac.config(state="normal")
    btn_convertir.config(state="normal")
    entry_pwm.config(state="normal")
    btn_pwm.config(state="normal")
    
    # Habilitar/Deshabilitar basado en la selección
    if seleccion == "1":
        entry_dac.config(state="disabled")
        btn_convertir.config(state="disabled")
        entry_pwm.config(state="disabled")
        btn_pwm.config(state="disabled")
    elif seleccion == "2":
        entry_opcion1.config(state="disabled")
        btn_sumar.config(state="disabled")
        entry_pwm.config(state="disabled")
        btn_pwm.config(state="disabled")
    elif seleccion == "3":
        entry_opcion1.config(state="disabled")
        btn_sumar.config(state="disabled")
        entry_dac.config(state="disabled")
        btn_convertir.config(state="disabled")

# Ventana principal
root= ThemedTk(theme= "black")#asignamos el tema para nuestra ventana
root.config(width=1000, height=1000)#definimos el ancho y largo de la ventana
root.title("practica1 ")#asignamos un titulo para la ventana



# Crear las pestañas (tabs)
tab_control = ttk.Notebook(root)
tab1 = ttk.Frame(tab_control)
tab2 = ttk.Frame(tab_control)
tab3 = ttk.Frame(tab_control)

tab_control.add(tab1, text='Conexión')
tab_control.add(tab2, text='Interacción')
tab_control.add(tab3, text='tab 3')

tab_control.pack(expand=1, fill="both")

# Cargar imágenes de LED (verde y rojo)
img_led_green = ImageTk.PhotoImage(Image.open("ledgre.png").resize((50, 50)))
img_led_red = ImageTk.PhotoImage(Image.open("ledred.png").resize((50, 50)))

# --- Tab 1 --- 
label_port = ttk.Label(tab1, text="Port:")
label_port.grid(column=0, row=0, padx=10, pady=10)

# Combobox para seleccionar puertos COM disponibles
ports = serial_ports()
combobox_ports = ttk.Combobox(tab1)
combobox_ports['values'] = ports if ports else ["No se encontraron puertos"]
combobox_ports.grid(column=1, row=0, padx=1, pady=10)

# Combobox para seleccionar velocidad de bits por segundo
label_baud = ttk.Label(tab1, text="velocidad:")
label_baud.grid(column=2, row=0, padx=8, pady=10)

combobox_baud = ttk.Combobox(tab1, values=["9600", "115200", "19200", "57600"])
combobox_baud.grid(column=3, row=0, padx=0, pady=10)

# Botón para conectar
btn_conectar = ttk.Button(tab1, text="Conectar", command=conectar)
btn_conectar.grid(column=0, row=1, columnspan=4, padx=10, pady=10)

# Imagen del LED (verde o rojo) que indica el estado de conexión
label_led = ttk.Label(tab1, image=img_led_red)  # Inicialmente el LED está en rojo (desconectado)
label_led.grid(column=3, row=1, padx=10, pady=10)

# Botones para encender y apagar el LED
btn_led_on = ttk.Button(tab1, text="LED ON", command=led_on)
btn_led_on.grid(column=0, row=2, padx=10, pady=10)

btn_led_off = ttk.Button(tab1, text="LED OFF", command=led_off)
btn_led_off.grid(column=1, row=2, padx=10, pady=10)

# --- Tab 2 --- 
spinbox_opcion = ttk.Spinbox(tab2, from_=1, to=3)
spinbox_opcion.grid(column=0, row=0, padx=10, pady=10)

btn_confirmar = ttk.Button(tab2, text="Confirmar", command=deshabilitar_opciones)
btn_confirmar.grid(column=1, row=0, padx=10, pady=10)

# Opción 1: sumar uno
label_opcion1 = ttk.Label(tab2, text="Opción 1:")
label_opcion1.grid(column=0, row=1, padx=10, pady=10)

entry_opcion1 = ttk.Entry(tab2)
entry_opcion1.grid(column=1, row=1, padx=10, pady=10)

label_resultado = ttk.Label(tab2, text="Resultado:")  # Mostrar el resultado de la suma aquí
label_resultado.grid(column=3, row=1, padx=0.1, pady=10)

# Botón para sumar 1 sin cambiar el entry
btn_sumar = ttk.Button(tab2, text="Sumar 1", command=lambda: sumar_uno(entry_opcion1, label_resultado))
btn_sumar.grid(column=2, row=1, padx=10, pady=10)

# Opción 2: DAC
label_opcion2 = ttk.Label(tab2, text="Opción 2 (DAC):")
label_opcion2.grid(column=0, row=2, padx=10, pady=10)

entry_dac = ttk.Entry(tab2)
entry_dac.grid(column=1, row=2, padx=10, pady=10)

btn_convertir = ttk.Button(tab2, text="Convertir", command=convertir_dac)  # Actualizado para usar la función convertir_dac
btn_convertir.grid(column=2, row=2, padx=10, pady=10)

# Opción 3: PWM
label_opcion3 = ttk.Label(tab2, text="Opción 3 (PWM):")
label_opcion3.grid(column=0, row=3, padx=10, pady=10)

entry_pwm = ttk.Entry(tab2)
entry_pwm.grid(column=1, row=3, padx=10, pady=10)

btn_pwm = ttk.Button(tab2, text="Configurar PWM", command=configurar_pwm)
btn_pwm.grid(column=2, row=3, padx=10, pady=10)

# --- Tab 3 ---
# Puedes añadir más controles o funcionalidad en esta pestaña según sea necesario

# Iniciar la aplicación
root.mainloop()
