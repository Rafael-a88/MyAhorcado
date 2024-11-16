import random
import pygame
import sys
import mysql.connector
from tkinter import simpledialog, StringVar, ttk
import tkinter as tk

# Inicializar Pygame
pygame.init()
pygame.mixer.init()

# Añadir un favicon
favicon = pygame.image.load('ahorcado_6.png')
pygame.display.set_icon(favicon)

# Carga la música
pygame.mixer.music.load('Su Turno.ogg')
pygame.mixer.music.play(-1)

# Configuración de la pantalla
ancho_pantalla = 900
alto_pantalla = 700
pantalla = pygame.display.set_mode((ancho_pantalla, alto_pantalla))
pygame.display.set_caption("Juego del Ahorcado")

# Cargar la fuente Roboto
fuente = pygame.font.Font("Roboto-Regular.ttf", 54)
fuente_chica = pygame.font.Font("Roboto-Regular.ttf", 36)

# Colores
WHITE = (255, 255, 255)
BLUE = (10, 58, 194)
BLACK = (0, 0, 0)
ROJO = (158, 3, 3)
ORO = (168, 145, 89)
VERDE = (2, 111, 0)

# Variables de categoría
categorias = ["Frutas", "Conceptos_informaticos", "Nombres_persona"]

def conexion():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="ahorcado"
    )

def obtener_palabras(categoria):
    """Recupera una lista de palabras de la base de datos según la categoría seleccionada."""
    bd = conexion()
    cursor = bd.cursor()
    if categoria == 'Frutas':
        cursor.execute("SELECT nombre FROM Frutas")
    elif categoria == 'Conceptos_informaticos':
        cursor.execute("SELECT nombre FROM Conceptos_informaticos")
    elif categoria == 'Nombres_persona':
        cursor.execute("SELECT nombre FROM Nombres_persona")

    palabras = cursor.fetchall()
    cursor.close()
    bd.close()
    return [palabra[0] for palabra in palabras]

def actualizar_victorias(usuario):
    """Actualiza el contador de partidas ganadas del usuario en la base de datos."""
    bd = conexion()
    cursor = bd.cursor()
    cursor.execute("UPDATE usuarios SET partidas_ganadas = partidas_ganadas + 1 WHERE nombre = %s", (usuario,))
    bd.commit()
    cursor.close()
    bd.close()

def actualizar_derrotas(usuario):
    """Actualiza el contador de partidas perdidas del usuario en la base de datos."""
    bd = conexion()
    cursor = bd.cursor()
    cursor.execute("UPDATE usuarios SET partidas_perdidas = partidas_perdidas + 1 WHERE nombre = %s", (usuario,))
    bd.commit()
    cursor.close()
    bd.close()

def obtener_datos_usuario(usuario):
    """Recupera los datos del usuario (partidas ganadas y perdidas) desde la base de datos."""
    bd = conexion()
    cursor = bd.cursor()
    cursor.execute("SELECT SUM(partidas_ganadas), SUM(partidas_perdidas) FROM usuarios WHERE nombre = %s", (usuario,))
    datos = cursor.fetchone()
    if datos is None or datos[0] is None or datos[1] is None:
        # Si el usuario no existe, insertarlo en la base de datos
        cursor.execute("INSERT INTO usuarios (nombre, partidas_ganadas, partidas_perdidas) VALUES (%s, 0, 0)", (usuario,))
        bd.commit()
        datos = (0, 0)
    cursor.close()
    bd.close()
    return datos

def mostrar_imagen(intentos):
    """Carga y muestra una imagen del ahorcado correspondiente al número de intentos fallidos."""
    ruta_imagen = f"ahorcado_{intentos}.png"
    imagen = pygame.image.load(ruta_imagen)

    # Calcular la posición para centrar la imagen en la parte inferior
    x = ancho_pantalla // 2 - imagen.get_width() // 2
    y = alto_pantalla - imagen.get_height() - 20  # 20 píxeles de margen desde el fondo

    pantalla.blit(imagen, (x, y))
    pygame.display.flip()

def mostrar_interfaz(usuario, categoria, partidas_ganadas, partidas_perdidas):
    pantalla.fill(ORO)
    texto_titulo = fuente.render("El juego del Ahorcado", True, BLUE)
    pantalla.blit(texto_titulo, (ancho_pantalla // 2 - texto_titulo.get_width() // 2, 50))

    # Mostrar el nombre del usuario
    texto_nombre = fuente_chica.render("Nombre: " + usuario, True, BLACK)
    pantalla.blit(texto_nombre, (330, 150))

    # Renderizar partidas ganadas en verde
    texto_ganadas = fuente_chica.render(f"Ganadas: {partidas_ganadas}", True, VERDE)
    # Renderizar partidas perdidas en rojo
    texto_perdidas = fuente_chica.render(f"Perdidas: {partidas_perdidas}", True, ROJO)

    # Posición inicial para las estadísticas
    x_pos = 250
    pantalla.blit(texto_ganadas, (x_pos, 200))
    # Ajustar la posición para las partidas perdidas
    x_pos += texto_ganadas.get_width() + 20  # Espacio entre las dos estadísticas
    pantalla.blit(texto_perdidas, (x_pos, 200))

    pygame.display.flip()

def mostrar_resultado_final(adivinada, palabra, usuario):
    """Muestra el resultado del juego y permite reiniciar."""
    pantalla.fill(WHITE)
    if "_" not in adivinada:
        texto_resultado = fuente.render("¡Ganaste! La palabra era: " + palabra, True, VERDE)
        actualizar_victorias(usuario)
    else:
        texto_resultado = fuente.render("Perdiste. La palabra era: " + palabra, True, ROJO)
        actualizar_derrotas(usuario)

    pantalla.blit(texto_resultado, (ancho_pantalla // 2 - texto_resultado.get_width() // 2, alto_pantalla // 2 - texto_resultado.get_height() // 2))

    # Crear botón de reinicio
    boton_reinicio = pygame.Rect(ancho_pantalla // 2 - 100, alto_pantalla // 2 + 50, 200, 50)
    pygame.draw.rect(pantalla, BLUE, boton_reinicio)

    # Renderizar el texto del botón
    texto_reinicio = fuente_chica.render("Reiniciar", True, WHITE)
    centrado = texto_reinicio.get_rect(center=boton_reinicio.center)  # Centrar el texto en el botón
    pantalla.blit(texto_reinicio, centrado)

    pygame.display.flip()

    # Esperar a que el usuario haga clic en el botón
    reiniciar = False
    while not reiniciar:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if boton_reinicio.collidepoint(event.pos):
                    reiniciar = True

def jugar(usuario, categoria):
    partidas_ganadas, partidas_perdidas = obtener_datos_usuario(usuario)
    while True:  # Bucle para permitir reiniciar el juego
        lista_palabras = obtener_palabras(categoria)
        palabra = random.choice(lista_palabras).upper()
        adivinada = "_" * len(palabra)
        intentos = 6

        print("¡Comienza el juego! Tienes {} intentos.".format(intentos))
        mostrar_imagen(0)

        while intentos > 0 and "_" in adivinada:
            # Actualizar las estadísticas antes de mostrar la interfaz
            partidas_ganadas, partidas_perdidas = obtener_datos_usuario(usuario)
            mostrar_interfaz(usuario, categoria, partidas_ganadas, partidas_perdidas)

            texto_palabra = fuente.render("Palabra: " + adivinada, True, BLACK)
            pantalla.blit(texto_palabra, (ancho_pantalla // 2 - texto_palabra.get_width() // 2, alto_pantalla // 2 - 50))

            texto_intentos = fuente_chica.render("Intentos restantes: {}".format(intentos), True, BLACK)
            pantalla.blit(texto_intentos, (ancho_pantalla // 2 - texto_intentos.get_width() // 2, alto_pantalla // 2))

            pygame.display.flip()

            intento = None
            while intento is None:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.unicode.isalpha() and len(event.unicode) == 1:
                            intento = event.unicode.upper()

            if intento in palabra:
                adivinada = "".join([intento if palabra[i] == intento else adivinada[i] for i in range(len(palabra))])
                print("¡Correcto!")
            else:
                intentos -= 1
                print("Incorrecto. Te quedan {} intentos.".format(intentos))
                mostrar_imagen(6 - intentos)
                pygame.time.delay(1000)

        mostrar_resultado_final(adivinada, palabra, usuario)


def obtener_nombre_usuario():
    """Crea una ventana de Tkinter para solicitar el nombre del usuario."""
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal
    usuario = simpledialog.askstring("Nombre de Usuario", "Introduce tu nombre de usuario:")
    root.destroy()  # Cierra la ventana de entrada
    return usuario

def seleccionar_categoria():
    """Crea un desplegable para seleccionar la categoría."""
    root = tk.Tk()
    root.title("Selecciona la Categoría")

    # Variable para la categoría seleccionada
    categoria_var = StringVar()
    categorias = ["Frutas", "Conceptos_informaticos", "Nombres_persona"]

    # Crear el combobox
    combo = ttk.Combobox(root, textvariable=categoria_var, values=categorias)
    combo.pack(pady=20)
    combo.current(0)  # Seleccionar la primera categoría por defecto

    # Botón para confirmar la selección
    def confirmar():
        root.destroy()

    boton_confirmar = tk.Button(root, text="Confirmar", command=confirmar)
    boton_confirmar.pack(pady=10)

    root.mainloop()

    return categoria_var.get()

def main():
    """Función principal que solicita el nombre del usuario y llama a jugar()."""
    usuario = obtener_nombre_usuario()
    if usuario:
        categoria = seleccionar_categoria()
        jugar(usuario, categoria)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
