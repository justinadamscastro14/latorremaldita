import pygame
import random
import math
from src.ai.behavior_tree import *
from src.ai.astar import astar
from src.utils.constants import *

class Enemy:
    def __init__(self, x, y, level_map, walkable_tiles, image=None):
        self.rect = pygame.Rect(x, y, ENEMY_SIZE, ENEMY_SIZE)
        self.health = 50
        self.speed = ENEMY_SPEED
        self.level_map = level_map
        self.walkable_tiles = walkable_tiles
        self.state = "patrol"
        self.patrol_point = None
        self.path = []
        self.last_path_update = 0
        
        # Imagen del enemigo
        self.image = image
        
        # Usar un color en lugar de una imagen
        self.color = RED  # Rojo para los enemigos
        
        # Crear árbol de comportamiento
        self.behavior_tree = self.create_behavior_tree()
    
    def create_behavior_tree(self):
        # Crear nodos de acción
        detect_player = DetectPlayer()
        chase_player = ChasePlayer()
        patrol = Patrol()
        
        # Crear árbol
        chase_sequence = Sequence([detect_player, chase_player])
        root = Selector([chase_sequence, patrol])
        
        return root
    
    def update(self, player):
        # Ejecutar árbol de comportamiento
        self.behavior_tree.run(self, player)
    
    def can_see_player(self, player):
        # Calcular distancia al jugador
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        distance = math.sqrt(dx * dx + dy * dy)
        
        # Comprobar si el jugador está dentro del radio de detección
        if distance <= ENEMY_DETECTION_RADIUS:
            # Comprobar si hay línea de visión (sin paredes en medio)
            return self.has_line_of_sight(player)
        
        return False
    
    def has_line_of_sight(self, player):
        # Implementación simple de línea de visión
        # En un juego real, se comprobaría si hay paredes entre el enemigo y el jugador
        start_x, start_y = self.rect.center
        end_x, end_y = player.rect.center
        
        # Convertir a coordenadas de tile
        start_tile_x, start_tile_y = start_x // TILE_SIZE, start_y // TILE_SIZE
        end_tile_x, end_tile_y = end_x // TILE_SIZE, end_y // TILE_SIZE
        
        # Algoritmo de Bresenham para trazar una línea
        dx = abs(end_tile_x - start_tile_x)
        dy = abs(end_tile_y - start_tile_y)
        sx = 1 if start_tile_x < end_tile_x else -1
        sy = 1 if start_tile_y < end_tile_y else -1
        err = dx - dy
        
        x, y = start_tile_x, start_tile_y
        
        while x != end_tile_x or y != end_tile_y:
            if 0 <= y < len(self.level_map) and 0 <= x < len(self.level_map[0]):
                if self.level_map[y][x] == 1:  # Hay una pared
                    return False
            
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x += sx
            if e2 < dx:
                err += dx
                y += sy
        
        return True
    
    def chase_player(self, player):
        # Actualizar camino cada cierto tiempo para no sobrecargar
        current_time = pygame.time.get_ticks()
        if current_time - self.last_path_update > 500:  # Actualizar cada 500ms
            self.last_path_update = current_time
            
            # Convertir posiciones a coordenadas de tile
            start_tile = (self.rect.centerx // TILE_SIZE, self.rect.centery // TILE_SIZE)
            end_tile = (player.rect.centerx // TILE_SIZE, player.rect.centery // TILE_SIZE)
            
            # Encontrar camino con A*
            self.path = astar(start_tile, end_tile, self.level_map)
        
        # Seguir el camino si existe
        if self.path and len(self.path) > 0:
            next_tile = self.path[0]
            target_x = next_tile[0] * TILE_SIZE + TILE_SIZE // 2
            target_y = next_tile[1] * TILE_SIZE + TILE_SIZE // 2
            
            # Mover hacia el siguiente punto del camino
            dx = target_x - self.rect.centerx
            dy = target_y - self.rect.centery
            
            # Normalizar vector de dirección
            length = max(1, math.sqrt(dx * dx + dy * dy))
            dx = dx / length * self.speed
            dy = dy / length * self.speed
            
            # Actualizar posición
            self.rect.x += dx
            self.rect.y += dy
            
            # Si llegamos al tile, avanzar al siguiente punto del camino
            if abs(self.rect.centerx - target_x) < self.speed and abs(self.rect.centery - target_y) < self.speed:
                self.path.pop(0)
    
    def patrol(self):
        # Si no hay punto de patrulla o se ha alcanzado, elegir uno nuevo
        if self.patrol_point is None or (
            abs(self.rect.centerx - self.patrol_point[0]) < self.speed and 
            abs(self.rect.centery - self.patrol_point[1]) < self.speed
        ):
            self.choose_patrol_point()
        
        # Mover hacia el punto de patrulla
        if self.patrol_point:
            dx = self.patrol_point[0] - self.rect.centerx
            dy = self.patrol_point[1] - self.rect.centery
            
            # Normalizar vector de dirección
            length = max(1, math.sqrt(dx * dx + dy * dy))
            dx = dx / length * self.speed
            dy = dy / length * self.speed
            
            # Actualizar posición
            new_rect = self.rect.copy()
            new_rect.x += dx
            new_rect.y += dy
            
            # Comprobar colisiones con paredes
            tile_x = new_rect.centerx // TILE_SIZE
            tile_y = new_rect.centery // TILE_SIZE
            
            if 0 <= tile_y < len(self.level_map) and 0 <= tile_x < len(self.level_map[0]):
                if self.level_map[tile_y][tile_x] != 1:  # Si no es una pared
                    self.rect = new_rect
    
    def choose_patrol_point(self):
        # Elegir un punto aleatorio dentro del radio de patrulla
        for _ in range(10):  # Intentar 10 veces encontrar un punto válido
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(0, ENEMY_PATROL_RADIUS)
            
            target_x = self.rect.centerx + math.cos(angle) * distance
            target_y = self.rect.centery + math.sin(angle) * distance
            
            # Convertir a coordenadas de tile
            tile_x = int(target_x // TILE_SIZE)
            tile_y = int(target_y // TILE_SIZE)
            
            # Comprobar si el punto es válido (dentro del mapa y no es una pared)
            if (0 <= tile_y < len(self.level_map) and 
                0 <= tile_x < len(self.level_map[0]) and 
                self.level_map[tile_y][tile_x] != 1):
                
                self.patrol_point = (target_x, target_y)
                return
        
        # Si no se encuentra un punto válido, mantener el punto actual
        if not self.patrol_point:
            self.patrol_point = (self.rect.centerx, self.rect.centery)
    
    def take_damage(self, amount):
        self.health -= amount
    
    def draw(self, screen):
        if self.image:
            # Si hay imagen disponible, usarla
            screen.blit(self.image, self.rect.topleft)
        else:
            # Fallback: dibujar rectángulo si no hay imagen
            pygame.draw.rect(screen, self.color, self.rect)
        
        # Dibujar barra de salud
        health_percentage = max(0, self.health / 50)
        bar_width = ENEMY_SIZE
        pygame.draw.rect(screen, RED, (self.rect.x, self.rect.y - 10, bar_width, 5))
        pygame.draw.rect(screen, GREEN, (self.rect.x, self.rect.y - 10, bar_width * health_percentage, 5))


class Boss(Enemy):
    def __init__(self, x, y, level_map, walkable_tiles, image=None):
        super().__init__(x, y, level_map, walkable_tiles, image)
        self.health = 150
        self.speed = ENEMY_SPEED * 0.8  # Más lento pero más fuerte
        
        # Usar un color diferente para el jefe
        self.color = (150, 0, 150)  # Púrpura para el jefe
        
        # Ajustar rectángulo para que sea más grande
        self.rect.width = ENEMY_SIZE * 1.5
        self.rect.height = ENEMY_SIZE * 1.5
        
        # Ataques especiales
        self.special_attack_cooldown = 0
    
    def update(self, player):
        super().update(player)
        
        # Actualizar cooldown de ataque especial
        if self.special_attack_cooldown > 0:
            self.special_attack_cooldown -= 1
    
    def chase_player(self, player):
        super().chase_player(player)
        
        # Ataque especial si está cerca del jugador y el cooldown lo permite
        if self.special_attack_cooldown <= 0:
            dx = player.rect.centerx - self.rect.centerx
            dy = player.rect.centery - self.rect.centery
            distance = math.sqrt(dx * dx + dy * dy)
            
            if distance < ENEMY_SIZE * 3:
                self.special_attack_cooldown = 120  # 2 segundos de cooldown
                # El ataque especial se implementaría aquí
                # Por ejemplo, podría ser un ataque en área o un dash hacia el jugador
    
    def draw(self, screen):
        if self.image:
            # Si hay imagen disponible, usarla (escalada al tamaño del jefe)
            scaled_image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))
            screen.blit(scaled_image, self.rect.topleft)
        else:
            # Fallback: dibujar rectángulo si no hay imagen
            pygame.draw.rect(screen, self.color, self.rect)
        
        # Dibujar barra de salud
        health_percentage = max(0, self.health / 150)
        bar_width = self.rect.width
        pygame.draw.rect(screen, RED, (self.rect.x, self.rect.y - 10, bar_width, 5))
        pygame.draw.rect(screen, GREEN, (self.rect.x, self.rect.y - 10, bar_width * health_percentage, 5))