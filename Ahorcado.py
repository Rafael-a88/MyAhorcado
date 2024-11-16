import random
import mysql.connector
import pygame
import sys

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
screen_width = 900
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Juego del Ahorcado")

# Cargar la fuente
font = pygame.font.Font(None, 54)
small_font = pygame.font.Font(None, 36)

# Colores
WHITE = (255, 255, 255)
BLUE = (10, 50, 100)
BLACK = (0,0,0)


def main():
    running = True

    while running:
        screen.fill(WHITE)  # Fondo blanco

        # Título del juego - Colocar lo más arriba posible
        title_text = font.render("Juego del Ahorcado", True, BLUE)
        screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 20))

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


if __name__ == "__main__":
    main()
