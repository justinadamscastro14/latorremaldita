import pygame
from src.utils.constants import *

class Menu:
    def __init__(self, screen, game):
        self.screen = screen
        self.game = game
        self.font_large = pygame.font.SysFont(None, 72)
        self.font_medium = pygame.font.SysFont(None, 48)
        self.font_small = pygame.font.SysFont(None, 36)
        
        # Comentamos la carga de música para evitar errores
        # pygame.mixer.music.load(MENU_MUSIC)
        # pygame.mixer.music.set_volume(0.5)
        # pygame.mixer.music.play(-1)
        
        # Opciones del menú
        self.options = ["Iniciar Juego", "Salir"]
        self.selected_option = 0
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                if self.selected_option == 0:  # Iniciar Juego
                    # pygame.mixer.music.stop()
                    return "game"
                elif self.selected_option == 1:  # Salir
                    pygame.quit()
                    exit()
        
        return None
    
    def handle_game_over_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                # pygame.mixer.music.stop()
                return "game"
            elif event.key == pygame.K_m:
                # pygame.mixer.music.load(MENU_MUSIC)
                # pygame.mixer.music.play(-1)
                return "menu"
        
        return None
    
    def update(self):
        pass
    
    def update_game_over(self):
        pass
    
    def update_victory(self):
        pass
    
    def draw(self):
        # Dibujar título
        title = self.font_large.render("LA TORRE MALDITA", True, RED)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        self.screen.blit(title, title_rect)
        
        # Dibujar opciones
        for i, option in enumerate(self.options):
            color = WHITE if i != self.selected_option else GREEN
            text = self.font_medium.render(option, True, color)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 60))
            self.screen.blit(text, text_rect)
        
        # Dibujar instrucciones
        instructions = self.font_small.render("Usa las flechas para moverte y ESPACIO para atacar", True, WHITE)
        instructions_rect = instructions.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 3 // 4))
        self.screen.blit(instructions, instructions_rect)
    
    def draw_game_over(self):
        # Dibujar mensaje de game over
        game_over = self.font_large.render("GAME OVER", True, RED)
        game_over_rect = game_over.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        self.screen.blit(game_over, game_over_rect)
        
        # Dibujar opciones
        restart = self.font_medium.render("Presiona R para reiniciar", True, WHITE)
        restart_rect = restart.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(restart, restart_rect)
        
        menu = self.font_medium.render("Presiona M para volver al menú", True, WHITE)
        menu_rect = menu.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
        self.screen.blit(menu, menu_rect)
    
    def draw_victory(self):
        # Dibujar mensaje de victoria
        victory = self.font_large.render("¡VICTORIA!", True, GREEN)
        victory_rect = victory.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        self.screen.blit(victory, victory_rect)
        
        # Dibujar mensaje
        message = self.font_medium.render("Has escapado de la Torre Maldita", True, WHITE)
        message_rect = message.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(message, message_rect)
        
        # Dibujar opciones
        restart = self.font_medium.render("Presiona R para jugar de nuevo", True, WHITE)
        restart_rect = restart.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
        self.screen.blit(restart, restart_rect)
        
        menu = self.font_medium.render("Presiona M para volver al menú", True, WHITE)
        menu_rect = menu.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 120))
        self.screen.blit(menu, menu_rect) 