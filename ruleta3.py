import tkinter as tk
from tkinter import messagebox, ttk
import random
import math
import threading
from playsound import playsound

orden_numeros_ruleta = [
    0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6,
    27, 13, 36, 11, 30, 8, 23, 10, 5, 24,
    16, 33, 1, 20, 14, 31, 9, 22, 18, 29,
    7, 28, 12, 35, 3, 26
]

rojos = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}
negros = {2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35}

class RuletaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎰 Ruleta Realista")
        self.dinero = 0
        self.numeros = orden_numeros_ruleta
        self.canvas_size = 400
        self.main_frame = tk.Frame(root, bg="#1e1e2f")
        self.main_frame.pack(padx=20, pady=20)

        self.controles = tk.Frame(self.main_frame, bg="#1e1e2f")
        self.controles.grid(row=0, column=0, padx=10, sticky="n")

        # Depósito
        tk.Label(self.controles, text="Depositar:", fg="white", bg="#1e1e2f", font=("Arial", 10)).pack()
        self.entry_deposito = tk.Entry(self.controles)
        self.entry_deposito.pack(pady=2)
        tk.Button(self.controles, text="💰 Depositar", command=self.depositar, bg="#4CAF50", fg="white").pack(pady=5)

        tk.Label(self.controles, text="Apostar:", fg="white", bg="#1e1e2f", font=("Arial", 10)).pack()
        self.entry_apuesta = tk.Entry(self.controles)
        self.entry_apuesta.pack()

        # Opciones para seleccionar número o color
        self.apostar_numero_var = tk.BooleanVar()
        self.apostar_color_var = tk.BooleanVar()

        # Crear combobox para elegir el número
        tk.Label(self.controles, text="Selecciona un número:", fg="white", bg="#1e1e2f").pack(pady=5)
        self.combo_numero = ttk.Combobox(self.controles, values=["Ninguno"] + [str(num) for num in self.numeros], state="normal")
        self.combo_numero.set("Ninguno")
        self.combo_numero.pack(pady=5)

        # Crear combobox para elegir el color
        tk.Label(self.controles, text="Selecciona un color:", fg="white", bg="#1e1e2f").pack(pady=5)
        self.combo_color = ttk.Combobox(self.controles, values=["Rojo", "Negro", "Verde", "Ninguno"], state="normal")
        self.combo_color.set("Ninguno")
        self.combo_color.pack(pady=5)

        self.label_dinero = tk.Label(self.controles, text=f"Dinero: ${self.dinero}", fg="yellow", bg="#1e1e2f", font=("Arial", 12, "bold"))
        self.label_dinero.pack(pady=10)

        self.boton_girar = tk.Button(self.controles, text="🎡 Girar Ruleta", command=self.jugar, bg="#2196F3", fg="white")
        self.boton_girar.pack()

        self.resultado = tk.Label(self.controles, text="", font=("Arial", 10, "bold"), bg="#1e1e2f", fg="white")
        self.resultado.pack(pady=10)

        self.canvas = tk.Canvas(self.main_frame, width=self.canvas_size, height=self.canvas_size, bg="darkgreen")
        self.canvas.grid(row=0, column=1, padx=20)

        self.angulo_bola = 0
        self.dibujar_ruleta()

    def depositar(self):
        try:
            monto = int(self.entry_deposito.get())
            if monto > 0:
                self.dinero += monto
                self.label_dinero.config(text=f"Dinero: ${self.dinero}")
                self.entry_deposito.delete(0, tk.END)
            else:
                raise ValueError
        except:
            messagebox.showerror("Error", "Monto de depósito inválido")

    def dibujar_ruleta(self):
        self.canvas.delete("all")
        centro = self.canvas_size // 2
        radio = centro - 10
        angulo_por_num = 360 / len(self.numeros)

        for i, num in enumerate(self.numeros):
            start = (i * angulo_por_num) % 360
            color = "green" if num == 0 else "red" if num in rojos else "black"
            self.canvas.create_arc(10, 10, self.canvas_size-10, self.canvas_size-10,
                                   start=start, extent=angulo_por_num, fill=color, outline="white")
            x = centro + (radio - 30) * math.cos(math.radians(start + angulo_por_num/2))
            y = centro - (radio - 30) * math.sin(math.radians(start + angulo_por_num/2))
            self.canvas.create_text(x, y, text=str(num), fill="white", font=("Arial", 8, "bold"))

    def dibujar_bola(self, angulo):
        centro = self.canvas_size // 2
        radio = centro - 10
        x = centro + radio * math.cos(math.radians(angulo))
        y = centro - radio * math.sin(math.radians(angulo))
        self.canvas.create_oval(x - 8, y - 8, x + 8, y + 8, fill="white", outline="black", width=2)

    def reproducir_sonido(self):
        try:
            playsound("bola3.mp3")
        except:
            print("⚠️ No se pudo reproducir el sonido. Asegúrate de tener 'bola.mp3'.")

    def jugar(self):
        try:
            apuesta = int(self.entry_apuesta.get())
            if apuesta <= 0 or apuesta > self.dinero:
                raise ValueError
        except:
            messagebox.showerror("Error", "Apuesta inválida")
            return

        # Obtener las selecciones de número y color
        self.numero_apostado = self.combo_numero.get().strip().lower()
        self.color_apostado = self.combo_color.get().strip().lower()

        # Validación para asegurarse de que solo uno esté seleccionado
        if self.numero_apostado != "ninguno" and self.color_apostado != "ninguno":
            messagebox.showerror("Error", "Selecciona solo un número o un color para apostar, pero no ambos.")
            return
        if self.numero_apostado == "ninguno" and self.color_apostado == "ninguno":
            messagebox.showerror("Error", "Debes seleccionar un número o un color para apostar.")
            return

        # Validación del número
        if self.numero_apostado != "ninguno":
            try:
                self.numero_apostado = int(self.numero_apostado)
                if self.numero_apostado not in self.numeros:
                    raise ValueError
            except:
                messagebox.showerror("Error", "Número inválido.")
                return
        else:
            self.numero_apostado = None

        # Validación del color
        if self.color_apostado != "ninguno" and self.color_apostado not in ["rojo", "negro", "verde"]:
            messagebox.showerror("Error", "Color inválido.")
            return
        elif self.color_apostado == "ninguno":
            self.color_apostado = None

        self.numero_ganador = random.choice(self.numeros)
        index_ganador = self.numeros.index(self.numero_ganador)
        self.angulo_objetivo = (index_ganador * (360 / len(self.numeros))) % 360
        self.angulo_total = self.angulo_objetivo + 360 * 5

        self.angulo_actual = 0
        self.paso = 0
        self.total_pasos = 100

        threading.Thread(target=self.reproducir_sonido, daemon=True).start()
        self.animar_bola(lambda: self.verificar_resultado(apuesta))

    def animar_bola(self, callback):
        if self.paso >= self.total_pasos:
            callback()
            return

        t = self.paso / self.total_pasos
        easing = (1 - (1 - t)**3)
        angulo_animado = self.angulo_actual = self.angulo_total * easing

        self.canvas.delete("all")
        self.dibujar_ruleta()
        self.dibujar_bola(angulo_animado)

        self.paso += 1
        self.root.after(30, lambda: self.animar_bola(callback))

    def verificar_resultado(self, apuesta):
        color_ganador = "verde" if self.numero_ganador == 0 else ("rojo" if self.numero_ganador in rojos else "negro")

        resultado = f"El número ganador es: {self.numero_ganador} ({color_ganador})"
        if self.numero_apostado == self.numero_ganador:
            self.dinero += apuesta * 35-apuesta
            resultado += f"\n¡Felicidades, ganaste! Tu ganancia es: ${apuesta * 35}"
        elif self.color_apostado == color_ganador:
            self.dinero += apuesta * 2-apuesta
            resultado += f"\n¡Felicidades, ganaste el color! Tu ganancia es: ${apuesta * 2}"
        else:
            self.dinero -= apuesta
            resultado += f"\nPerdiste. Has perdido: ${apuesta}"

        self.label_dinero.config(text=f"Dinero: ${self.dinero}")
        self.resultado.config(text=resultado)

# Configuración de la ventana principal
root = tk.Tk()
app = RuletaApp(root)
root.mainloop()
