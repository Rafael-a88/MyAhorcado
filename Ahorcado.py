import random
import mysql.connector
import pygame
import sys

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
ancho_pantalla = 900
alto_pantalla = 700
screen = pygame.display.set_mode((ancho_pantalla, alto_pantalla))
pygame.display.set_caption("Juego del Ahorcado")

# Cargar la fuente Roboto
fuente = pygame.font.Font("Roboto-Regular.ttf", 54)
fuente_chica = pygame.font.Font("Roboto-Regular.ttf", 36)

# Colores
WHITE = (255, 255, 255)
BLUE = (10, 50, 100)
BLACK = (0, 0, 0)

def main():
    running = True

    while running:
        screen.fill(WHITE)  # Fondo blanco

        # Título del juego - Colocar lo más arriba posible
        title_text = fuente.render("Juego del Ahorcado", True, BLUE)
        screen.blit(title_text, (ancho_pantalla // 2 - title_text.get_width() // 2, 20))

        # Esperar hasta que el jugador cierre la ventana
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()  # Actualizar la pantalla
        pygame.time.Clock().tick(30)  # Controlar el frame rate

    pygame.quit()
    sys.exit()

# ------------------- HASTA AQUI LA PARTE DE LA VENTANA PRINCIPAL ------------------- #

def conexion():
    return mysql.connector.connect(
        host="RafaBBDD",
        user="root",
        password="",
        database="Ahorcado"
    )

def obtener_palabras(categoria):
    """
    Recupera una lista de palabras de la base de datos según la categoría seleccionada.
    """
    bd = conexion()
    cursor = bd.cursor()
    if categoria == 'fruta':
        cursor.execute("SELECT nombre FROM frutas")
    elif categoria == 'concepto_informatico':
        cursor.execute("SELECT nombre FROM conceptos_informaticos")
    elif categoria == 'nombre_persona':
        cursor.execute("SELECT nombre FROM nombres_persona")

    palabras = cursor.fetchall()
    cursor.close()
    bd.close()
    return [palabra[0] for palabra in palabras]

def actualizar_victorias(usuario):
    """
    Actualiza el contador de partidas ganadas del usuario en la base de datos.
    """
    bd = conexion()
    cursor = bd.cursor()
    cursor.execute("UPDATE usuarios SET partidas_ganadas = partidas_ganadas + 1 WHERE nombre = %s", (usuario,))
    bd.commit()
    cursor.close()
    bd.close()

def actualizar_derrotas(usuario):
    """
    Actualiza el contador de partidas perdidas del usuario en la base de datos.
    """
    bd = conexion()
    cursor = bd.cursor()
    cursor.execute("UPDATE usuarios SET partidas_perdidas = partidas_perdidas + 1 WHERE nombre = %s", (usuario,))
    bd.commit()
    cursor.close()
    bd.close()


if __name__ == "__main__":
    main()
