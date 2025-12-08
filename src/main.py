import sys
import pygame
from game import Game
from ui.menu import Menu

def main():
    """
    Descripción
        FUNCIÓN: Punto de entrada principal. Gestiona el ciclo de vida de la aplicación,
        alternando entre el Menú Principal y el Juego.
    """
    app_running = True
    
    while app_running:
        # 1. Iniciar Menú
        menu = Menu()
        action = menu.run()
        
        # 2. Procesar acción del menú
        if action == "play":
            # Iniciar Juego
            # Nota: Game() reinicializa la ventana, lo cual es aceptable en esta transición
            game = Game()
            game.run()
            # Al salir del juego (game.run termina), el bucle while reinicia el menú
            # Si se desea salir completamente tras el juego, cambiar a app_running = False
        
        elif action == "exit":
            app_running = False
            
    # 3. Cierre final
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()