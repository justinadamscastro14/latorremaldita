#!/usr/bin/env python3
# La Torre Maldita - Juego principal

import pygame
import sys
from src.game import Game
from src.ui.menu import Menu
from src.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, TITLE, FPS

def main():
    # Inicializar pygame
    pygame.init()
    pygame.mixer.init()
    
    # Configurar la ventana
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()
    
    # Crear instancias del juego y el menú
    game = Game(screen)
    menu = Menu(screen, game)
    
    # Estado inicial
    current_state = "menu"
    
    # Bucle principal
    running = True
    while running:
        # Gestionar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Pasar eventos al estado actual
            if current_state == "menu":
                new_state = menu.handle_event(event)
                if new_state:
                    current_state = new_state
            elif current_state == "game":
                new_state = game.handle_event(event)
                if new_state:
                    current_state = new_state
            elif current_state == "game_over":
                new_state = menu.handle_game_over_event(event)
                if new_state:
                    if new_state == "game":
                        game.reset()
                    current_state = new_state
        
        # Actualizar
        if current_state == "menu":
            menu.update()
        elif current_state == "game":
            game_state = game.update()
            if game_state == "game_over":
                current_state = "game_over"
            elif game_state == "victory":
                current_state = "victory"
        elif current_state == "game_over":
            menu.update_game_over()
        elif current_state == "victory":
            menu.update_victory()
        
        # Renderizar
        screen.fill((0, 0, 0))
        
        if current_state == "menu":
            menu.draw()
        elif current_state == "game":
            game.draw()
        elif current_state == "game_over":
            menu.draw_game_over()
        elif current_state == "victory":
            menu.draw_victory()
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main() 