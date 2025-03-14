import pygame
import time
from src.utils.constants import *

class Player:
    def __init__(self, x, y, image=None):
        self.rect = pygame.Rect(x, y, PLAYER_SIZE, PLAYER_SIZE)
        self.health = PLAYER_HEALTH
        self.speed = PLAYER_SPEED
        self.direction = "down"
        self.is_moving = False
        self.is_attacking = False
        self.attack_rect = pygame.Rect(0, 0, PLAYER_SIZE * 1.5, PLAYER_SIZE * 1.5)
        self.attack_timer = 0
        self.is_invulnerable = False
        self.invulnerable_timer = 0
        
        # Imagen del jugador
        self.image = image
        
        # Poderes
        self.power_active = False
        self.power_time = 0
        self.power_start_time = 0
        
        # Usar un color en lugar de una imagen
        self.color = (0, 200, 0)  # Verde para el jugador
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.attack()
    
    def update(self, level_map, walkable_tiles):
        # Movimiento
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -self.speed
            self.direction = "left"
            self.is_moving = True
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = self.speed
            self.direction = "right"
            self.is_moving = True
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -self.speed
            self.direction = "up"
            self.is_moving = True
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = self.speed
            self.direction = "down"
            self.is_moving = True
        else:
            self.is_moving = False
        
        # Aplicar velocidad adicional si hay poder activo
        if self.power_active:
            dx *= 1.5
            dy *= 1.5
        
        # Comprobar colisiones con paredes
        new_rect = self.rect.copy()
        new_rect.x += dx
        new_rect.y += dy
        
        # Convertir posición de píxeles a coordenadas de tile
        tile_x1 = max(0, new_rect.left // TILE_SIZE)
        tile_y1 = max(0, new_rect.top // TILE_SIZE)
        tile_x2 = min(len(level_map[0]) - 1, new_rect.right // TILE_SIZE)
        tile_y2 = min(len(level_map) - 1, new_rect.bottom // TILE_SIZE)
        
        # Comprobar si hay colisión con paredes
        collision = False
        for y in range(tile_y1, tile_y2 + 1):
            for x in range(tile_x1, tile_x2 + 1):
                if level_map[y][x] == 1:  # 1 representa una pared
                    collision = True
                    break
            if collision:
                break
        
        # Actualizar posición si no hay colisión
        if not collision:
            self.rect = new_rect
        
        # Actualizar rectángulo de ataque
        self.update_attack_rect()
        
        # Actualizar temporizador de ataque
        if self.is_attacking:
            self.attack_timer -= 1
            if self.attack_timer <= 0:
                self.is_attacking = False
        
        # Actualizar temporizador de invulnerabilidad
        if self.is_invulnerable:
            self.invulnerable_timer -= 1
            if self.invulnerable_timer <= 0:
                self.is_invulnerable = False
        
        # Actualizar temporizador de poder
        if self.power_active:
            current_time = time.time()
            elapsed = current_time - self.power_start_time
            self.power_time = max(0, POWER_DURATION - elapsed)
            
            if self.power_time <= 0:
                self.power_active = False
    
    def update_attack_rect(self):
        # Actualizar posición del rectángulo de ataque según la dirección
        if self.direction == "up":
            self.attack_rect.midbottom = self.rect.midtop
        elif self.direction == "down":
            self.attack_rect.midtop = self.rect.midbottom
        elif self.direction == "left":
            self.attack_rect.midright = self.rect.midleft
        elif self.direction == "right":
            self.attack_rect.midleft = self.rect.midright
    
    def attack(self):
        if not self.is_attacking:
            self.is_attacking = True
            self.attack_timer = 10  # Duración del ataque en frames
    
    def take_damage(self, amount):
        if not self.is_invulnerable:
            self.health -= amount
            self.is_invulnerable = True
            self.invulnerable_timer = 60  # Invulnerabilidad por 1 segundo (60 frames)
    
    def heal(self, amount):
        self.health = min(PLAYER_HEALTH, self.health + amount)
    
    def activate_power(self):
        self.power_active = True
        self.power_start_time = time.time()
        self.power_time = POWER_DURATION
    
    def draw(self, screen):
        # Dibujar jugador con efecto de parpadeo si está invulnerable
        if not self.is_invulnerable or pygame.time.get_ticks() % 200 < 100:
            if self.image:
                # Si hay imagen disponible, usarla
                if self.power_active:
                    # Crear una copia con tinte azul para el poder activo
                    power_img = self.image.copy()
                    power_img.fill((0, 100, 255, 128), special_flags=pygame.BLEND_RGBA_MULT)
                    screen.blit(power_img, self.rect.topleft)
                else:
                    screen.blit(self.image, self.rect.topleft)
            else:
                # Fallback: dibujar rectángulo si no hay imagen
                if self.power_active:
                    pygame.draw.rect(screen, (0, 100, 255), self.rect)
                else:
                    pygame.draw.rect(screen, self.color, self.rect)
        
        # Dibujar área de ataque si está atacando
        if self.is_attacking:
            pygame.draw.rect(screen, RED, self.attack_rect, 2) 