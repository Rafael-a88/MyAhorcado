import random
import sys
import pygame
import tkinter as tk
from tkinter import StringVar, ttk
from base_datos import BaseDeDatos, GestorAhorcado

# Inicializar Pygame
pygame.init()  
pygame.mixer.init()  # Inicializa el módulo de mezcla de audio

# Configuración de la pantalla
ancho_pantalla = 900
alto_pantalla = 700
pantalla = pygame.display.set_mode((ancho_pantalla, alto_pantalla))  # Crea la ventana del juego
pygame.display.set_caption("Juego del Ahorcado")

# Cargar recursos
favicon = pygame.image.load('ahorcado_6.png')  # Carga el icono del juego
pygame.display.set_icon(favicon)
pygame.mixer.music.load('Su Turno.ogg')
pygame.mixer.music.play(-1)

# Cargar fuentes
fuente = pygame.font.Font("Roboto-Regular.ttf", 54)  # Fuente grande para el título
fuente_chica = pygame.font.Font("Roboto-Regular.ttf", 36)  # Fuente más pequeña para estadísticas

# Definición de colores
WHITE = (255, 255, 255)
BLUE = (10, 58, 194)
BLACK = (0, 0, 0)
ROJO = (158, 3, 3)
ORO = (168, 145, 89)
VERDE = (2, 111, 0)

# Variables de categoría
categorias = ["Frutas", "Conceptos_informaticos", "Nombres_persona"]

# Inicializar la base de datos y el gestor
db = BaseDeDatos()  # Instancia de la clase BaseDeDatos
gestor_ahorcado = GestorAhorcado(db)

# Funciones de visualización
def mostrar_imagen(intentos):
    """Carga y muestra una imagen del ahorcado correspondiente al número de intentos fallidos."""
    ruta_imagen = f"ahorcado_{intentos}.png"  # Ruta de la imagen según intentos
    imagen = pygame.image.load(ruta_imagen)  # Carga la imagen
    x = ancho_pantalla // 2 - imagen.get_width() // 2  # Centra la imagen horizontalmente
    y = alto_pantalla - imagen.get_height() - 20  # Posición vertical
    pantalla.blit(imagen, (x, y))  # Dibuja la imagen en la pantalla
    pygame.display.flip()  # Actualiza la pantalla

def mostrar_interfaz(usuario, categoria, partidas_ganadas, partidas_perdidas):
    """Muestra la interfaz del juego con estadísticas del usuario."""
    pantalla.fill(ORO)
    texto_titulo = fuente.render("El juego del Ahorcado", True, BLUE)
    pantalla.blit(texto_titulo, (ancho_pantalla // 2 - texto_titulo.get_width() // 2, 50))  # Centra el título

    texto_nombre = fuente_chica.render("Nombre: " + usuario, True, BLACK)  # Muestra el nombre del usuario
    pantalla.blit(texto_nombre, (330, 150))  # Posición del nombre

    texto_ganadas = fuente_chica.render(f"Ganadas: {partidas_ganadas}", True, VERDE)  # Muestra partidas ganadas
    texto_perdidas = fuente_chica.render(f"Perdidas: {partidas_perdidas}", True, ROJO)  # Muestra partidas perdidas

    x_pos = 250
    pantalla.blit(texto_ganadas, (x_pos, 200))  # Posición de partidas ganadas
    x_pos += texto_ganadas.get_width() + 20
    pantalla.blit(texto_perdidas, (x_pos, 200))  # Posición de partidas perdidas

    pygame.display.flip()  # Actualiza la pantalla

def mostrar_resultado_final(adivinada, palabra, usuario):
    """Muestra el resultado del juego y permite reiniciar."""
    pantalla.fill(WHITE)
    if "_" not in adivinada:  # Verifica si la palabra fue adivinada
        texto_resultado = fuente.render("¡Ganaste! La palabra era: " + palabra, True, VERDE)  # Mensaje de victoria
        gestor_ahorcado.actualizar_victorias(usuario)
    else:
        texto_resultado = fuente.render("Perdiste. La palabra era: " + palabra, True, ROJO)  # Mensaje de derrota
        gestor_ahorcado.actualizar_derrotas(usuario)

    # Centra el mensaje en la pantalla
    pantalla.blit(texto_resultado, (ancho_pantalla // 2 - texto_resultado.get_width() // 2, alto_pantalla // 2 - texto_resultado.get_height() // 2))

    # Botón para reiniciar el juego
    boton_reinicio = pygame.Rect(ancho_pantalla // 2 - 100, alto_pantalla // 2 + 50, 200, 50)
    pygame.draw.rect(pantalla, BLUE, boton_reinicio)  # Dibuja el botón

    texto_reinicio = fuente_chica.render("Reiniciar", True, WHITE)  # Texto del botón
    centrado = texto_reinicio.get_rect(center=boton_reinicio.center)  # Centra el texto en el botón
    pantalla.blit(texto_reinicio, centrado)  # Dibuja el texto en el botón

    pygame.display.flip()  # Actualiza la pantalla
    reiniciar = False
    while not reiniciar:  # Espera a que el usuario decida reiniciar
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if boton_reinicio.collidepoint(event.pos):  # Verifica si se hizo clic en el botón
                    reiniciar = True

# Función principal del juego
def jugar(usuario, categoria):
    partidas_ganadas, partidas_perdidas = gestor_ahorcado.obtener_datos_usuario(usuario)  # Obtiene estadísticas del usuario

    while True:
        lista_palabras = gestor_ahorcado.obtener_palabras(categoria)  # Obtiene palabras de la categoría seleccionada
        palabra = random.choice(lista_palabras).upper()
        adivinada = "_" * len(palabra)  # Inicializa la palabra adivinada con guiones bajos
        intentos = 6

        print("¡Comienza el juego! Tienes {} intentos.".format(intentos))
        mostrar_imagen(0)  # Muestra la imagen inicial del ahorcado

        while intentos > 0 and "_" in adivinada:  # Mientras haya intentos y la palabra no esté completamente adivinada
            partidas_ganadas, partidas_perdidas = gestor_ahorcado.obtener_datos_usuario(usuario)  # Actualiza estadísticas
            mostrar_interfaz(usuario, categoria, partidas_ganadas, partidas_perdidas)  # Muestra la interfaz

            texto_palabra = fuente.render("Palabra: " + adivinada, True, BLACK)  # Muestra la palabra adivinada
            pantalla.blit(texto_palabra, (ancho_pantalla // 2 - texto_palabra.get_width() // 2, alto_pantalla // 2 - 50))

            texto_intentos = fuente_chica.render("Intentos restantes: {}".format(intentos), True, BLACK)  # Muestra intentos restantes
            pantalla.blit(texto_intentos, (ancho_pantalla // 2 - texto_intentos.get_width() // 2, alto_pantalla // 2))

            pygame.display.flip()  # Actualiza la pantalla

            intento = None
            while intento is None:  # Espera a que el usuario ingrese una letra
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()  # Cierra Pygame
                        sys.exit()  # Sale del programa
                    if event.type == pygame.KEYDOWN:
                        if event.unicode.isalpha() and len(event.unicode) == 1:  # Verifica que se ingrese una letra
                            intento = event.unicode.upper()  # Convierte la letra a mayúscula

            if intento in palabra:  # Si el intento está en la palabra
                # Actualiza la palabra adivinada
                adivinada = "".join([intento if palabra[i] == intento else adivinada[i] for i in range(len(palabra))])
                print("¡Correcto!")  # Mensaje de acierto
            else:
                intentos -= 1  # Reduce el número de intentos
                print("Incorrecto. Te quedan {} intentos.".format(intentos))
                mostrar_imagen(6 - intentos)  # Muestra la imagen del ahorcado
                pygame.time.delay(1000)  # Espera un segundo antes de continuar

        mostrar_resultado_final(adivinada, palabra, usuario)

# Función de configuración inicial
def obtener_datos_iniciales():
    """Crea una ventana de Tkinter para solicitar el nombre del usuario y la categoría."""
    ventana_configuracion = tk.Tk()  # Crea la ventana de configuración
    ventana_configuracion.geometry(f"{ancho_pantalla}x{alto_pantalla}")
    ventana_configuracion.title("Configuración del Juego del Ahorcado")
    ventana_configuracion.config(bg="#a89159")

    # Centra la ventana en la pantalla
    ventana_configuracion.update_idletasks()
    width = ventana_configuracion.winfo_width()
    height = ventana_configuracion.winfo_height()
    x = (ventana_configuracion.winfo_screenwidth() // 2) - (width // 2) - 10
    y = (ventana_configuracion.winfo_screenheight() // 2) - (height // 2) - 30
    ventana_configuracion.geometry(f'{width}x{height}+{x}+{y}')

    usuario_var = StringVar()  # Variable para almacenar el nombre del usuario
    tk.Label(ventana_configuracion, text="Nombre de Usuario:", font=("Roboto", 24), bg="#a89159", fg="blue").pack(pady=(100, 0))
    entrada_usuario = tk.Entry(ventana_configuracion, textvariable=usuario_var, font=("Roboto", 20))  # Campo de entrada para el nombre
    entrada_usuario.pack(pady=(10, 50))

    categoria_var = StringVar()  # Variable para almacenar la categoría seleccionada
    tk.Label(ventana_configuracion, text="Selecciona la Categoría:", font=("Roboto", 24), bg="#a89159", fg="blue").pack(pady=10)
    combo = ttk.Combobox(ventana_configuracion, textvariable=categoria_var, values=categorias, font=("Roboto", 18), width=20)
    combo.pack(pady=10)  # Combo box para seleccionar la categoría
    combo.current(0)  # Establece la primera categoría como seleccionada

    def comenzar_juego():
        usuario = usuario_var.get()  # Obtiene el nombre del usuario
        categoria = categoria_var.get()  # Obtiene la categoría seleccionada
        if usuario and categoria:
            ventana_configuracion.destroy()
            jugar(usuario, categoria)  # Inicia el juego

    boton_jugar = tk.Button(ventana_configuracion, text="Jugar", command=comenzar_juego, bg="red", fg="white", width=20, height=2)  # Botón para comenzar el juego
    boton_jugar.pack(pady=20)

    ventana_configuracion.mainloop()  # Inicia el bucle principal de la ventana

# Función principal
def main():
    """Función principal que solicita el nombre del usuario y la categoría, luego llama a jugar()."""
    obtener_datos_iniciales()  # Llama a la función de configuración inicial
    db.cerrar_conexion()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
