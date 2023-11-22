from tkinter import *
import math

class Ventana:
    # Constructor
    def __init__(self):
        self.window = Tk()
        self.window.geometry('800x600')
        self.valor_zoom = 20.0  # valor del zoom con el que va a iniciar

        # Crear el lienzo a la izquierda
        self.canvas = Canvas(self.window, width=400, height=400, bg='green')
        self.canvas.pack(side=LEFT)

        # Crear un marco para los elementos a la derecha
        frame = Frame(self.window)
        frame.pack(side=RIGHT)

        # Definir ecuación de la recta = y = mx + b
        self.pendiente = Label(frame, text="Inserte el valor de la pendiente:")
        self.pendiente.pack(pady=5)
        self.caja_pendiente = Entry(frame)
        self.caja_pendiente.pack(pady=5)

        self.interseccion_y = Label(frame, text="Inserte el valor de la interseccion Y:")
        self.interseccion_y.pack(pady=5)
        self.caja_intersecciony = Entry(frame)
        self.caja_intersecciony.pack(pady=5)

        # Ecuación del círculo: (x - h)^2 + (y - k)^2 = r^2
        self.coordernada_x_centro = Label(frame, text="Inserte el valor de la coordenada del centro X:")
        self.coordernada_x_centro.pack(pady=5)
        self.caja_coordenadax = Entry(frame)
        self.caja_coordenadax.pack(pady=5)

        self.coordernada_y_centro = Label(frame, text="Inserte el valor de la coordenada del centro Y:")
        self.coordernada_y_centro.pack(pady=5)
        self.caja_coordenaday = Entry(frame)
        self.caja_coordenaday.pack(pady=5)

        self.radio = Label(frame, text="Inserte el valor de radio:")
        self.radio.pack(pady=5)
        self.caja_radio = Entry(frame)
        self.caja_radio.pack(pady=5)

        # Botón para cálculos
        self.sum_button = Button(frame, text="Calcular puntos", command=self.calcular)
        self.sum_button.pack(pady=10)

        # Etiqueta para mostrar el resultado
        self.punto1 = Label(frame, text="")
        self.punto1.pack(pady=5)

        self.punto2 = Label(frame, text="")
        self.punto2.pack(pady=5)

        # Botones de zoom
        self.zoom_in_button = Button(frame, text="Acercar", command=self.zoom_in)
        self.zoom_in_button.pack(pady=5)

        self.zoom_out_button = Button(frame, text="Alejar", command=self.zoom_out)
        self.zoom_out_button.pack(pady=5)

    def calcular(self):
        try:
            # Obtenemos valores y validamos si son números
            pendiente = float(self.caja_pendiente.get())
            interY = float(self.caja_intersecciony.get())
            coordenX = float(self.caja_coordenadax.get())
            coordenY = float(self.caja_coordenaday.get())
            radio = float(self.caja_radio.get())

            # Calcular los puntos de intersección
            # Igualamos la ecuación de la recta con la ecuación del círculo
            # (x - h)^2 + (mx + b - k)^2 = r^2
            # Expandimos y resolvemos para obtener las coordenadas x
            # A = 1 + m^2
            # B = -2h + 2mb - 2kb
            # C = h^2 + b^2 - 2by + k^2 - r^2
            A = 1 + pendiente**2
            B = -2 * coordenX + 2 * pendiente * (interY - coordenY)
            C = coordenX**2 + (interY - coordenY)**2 - radio**2

            # Calculamos el discriminante y luego validamos si hay puntos de intersección
            discriminante = B**2 - 4*A*C

            if discriminante < 0:
                self.punto1.config(text="No hay puntos de intersección")
            elif discriminante == 0:
                # Un punto de intersección (tangente)
                x = -B / (2*A)
                y = pendiente * x + interY
                self.punto1.config(text=f"Tangente: Un punto de intersección - Punto: ({x:.2f}, {y:.2f})")
            else:
                # Dos puntos de intersección (secantes)
                x1 = (-B + math.sqrt(discriminante)) / (2*A)
                x2 = (-B - math.sqrt(discriminante)) / (2*A)
                y1 = pendiente * x1 + interY
                y2 = pendiente * x2 + interY
                self.punto1.config(text=f"Secantes: Dos puntos de intersección - Punto 1: ({x1:.2f}, {y1:.2f}), Punto 2: ({x2:.2f}, {y2:.2f})")

                # Verificar si los puntos de intersección son iguales o tienen uno en común
                if (x1 == x2 and y1 == y2 or x1 == y1 or x2 == y2 or y1 == y2 or x1 == x2):
                    self.punto2.config(text="Hay puntos de interseccion en comun")
                else:
                    self.punto2.config(text="No hay ningún punto de intersección en común")

            # Llamar a la función para dibujar el plano cartesiano, la circunferencia y la recta
            self.plano(coordenX, coordenY, radio, pendiente, interY, discriminante, x1, x2, y1, y2)

        except ValueError:
            self.punto1.config(text="Por favor, ingresa números válidos.")

    def plano(self, coordenX, coordenY, radio, pendiente, interY, discriminante, x1, x2, y1, y2):
        # Borrar todo el lienzo antes de dibujar nuevamente
        self.canvas.delete("all")

        # Dibujar ejes X e Y en el lienzo 
        self.canvas.create_line(0, 200, 400, 200, fill='black', width=2)  # Eje X
        self.canvas.create_line(200, 0, 200, 400, fill='black', width=2)  # Eje Y

        # Escalar los elementos en el lienzo
        self.canvas.scale("all", 200, 200, self.valor_zoom, self.valor_zoom)

        # Dibujar la circunferencia en el plano cartesiano
        x0 = 200 + coordenX * self.valor_zoom
        y0 = 200 - coordenY * self.valor_zoom
        r = radio * self.valor_zoom
        self.canvas.create_oval(x0 - r, y0 - r, x0 + r, y0 + r, outline='blue')

        # Dibujar la recta en el plano cartesiano
        if discriminante >= 0:
            x1 = 200 + x1 * self.valor_zoom
            y1 = 200 - y1 * self.valor_zoom
            x2 = 200 + x2 * self.valor_zoom
            y2 = 200 - y2 * self.valor_zoom
            self.canvas.create_line(x1, y1, x2, y2, fill='red')

  


    def zoom_in(self):
        self.valor_zoom *= 1.1  # Aumentar el factor de zoom
        self.plano(None, None, None, None, None, None, None, None, None, None)

    def zoom_out(self):
        self.valor_zoom /= 1.1  # Disminuir el factor de zoom
        self.plano(None, None, None, None, None, None, None, None, None, None)

    def MostrarVentana(self):
        self.window.mainloop()

