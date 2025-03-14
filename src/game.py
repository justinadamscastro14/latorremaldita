import pygame
from src.player import Player
from src.level_generator import LevelGenerator
from src.enemy import Enemy, Boss
from src.utils.constants import *

def safe_play_music(music_file, loop=0):
    """Safely load and play a music file, handling errors if the file doesn't exist."""
    try:
        pygame.mixer.music.load(music_file)
        pygame.mixer.music.play(loop)
        return True
    except pygame.error:
        print(f"Warning: Could not load music file {music_file}")
        return False

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.level_generator = LevelGenerator()
        
        # Cargar imágenes
        self.load_images()
        
        self.reset()
        
        # Cargar sonidos
        self.load_sounds()
        
        # Cargar música
        safe_play_music(GAME_MUSIC)
        pygame.mixer.music.set_volume(0.5)
    
    def load_images(self):
        try:
            # Intentar cargar imágenes SVG con cairosvg
            try:
                import cairosvg
                import io
                
                def load_svg(path, size):
                    try:
                        png_data = cairosvg.svg2png(url=path, output_width=size, output_height=size)
                        return pygame.image.load(io.BytesIO(png_data))
                    except Exception as e:
                        print(f"Error converting SVG {path}: {e}")
                        return None
                
                print("Attempting to load SVG images using cairosvg...")
                self.images = {
                    'player': load_svg('assets/images/player.svg', TILE_SIZE),
                    'enemy': load_svg('assets/images/enemy.svg', TILE_SIZE),
                    'boss': load_svg('assets/images/boss.svg', TILE_SIZE),
                    'potion': load_svg('assets/images/potion.svg', TILE_SIZE),
                    'power': load_svg('assets/images/power.svg', TILE_SIZE),
                    'stairs': load_svg('assets/images/stairs.svg', TILE_SIZE),
                    'wall': load_svg('assets/images/wall.svg', TILE_SIZE),
                    'floor': load_svg('assets/images/floor.svg', TILE_SIZE)
                }
                
                # Filtrar imágenes que no se pudieron cargar
                failed_images = [k for k, v in self.images.items() if v is None]
                self.images = {k: v for k, v in self.images.items() if v is not None}
                
                if failed_images:
                    print(f"Warning: Could not load these SVG images: {', '.join(failed_images)}")
                
                if not self.images:
                    raise Exception("No se pudo cargar ninguna imagen SVG")
                    
            except ImportError:
                print("Warning: cairosvg not available. You can install it with: pip install cairosvg")
                raise Exception("cairosvg not available")
                
        except Exception as e:
            print(f"Warning: Could not load SVG images: {e}")
            print("Using colored rectangles with SVG patterns instead")
            
            # Crear representaciones mejoradas de cada elemento
            self.images = {}
            
            # Jugador (verde con forma de persona)
            player_surf = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
            # Cuerpo
            pygame.draw.circle(player_surf, (0, 180, 0), (TILE_SIZE//2, TILE_SIZE//3), TILE_SIZE//4)  # Cabeza
            pygame.draw.rect(player_surf, (0, 200, 0), (TILE_SIZE//3, TILE_SIZE//3, TILE_SIZE//3, TILE_SIZE//2))  # Cuerpo
            # Brazos
            pygame.draw.line(player_surf, (0, 180, 0), (TILE_SIZE//3, TILE_SIZE//2), (TILE_SIZE//6, TILE_SIZE//2), 3)  # Brazo izq
            pygame.draw.line(player_surf, (0, 180, 0), (TILE_SIZE*2//3, TILE_SIZE//2), (TILE_SIZE*5//6, TILE_SIZE//2), 3)  # Brazo der
            # Piernas
            pygame.draw.line(player_surf, (0, 180, 0), (TILE_SIZE*2//5, TILE_SIZE*5//6), (TILE_SIZE*2//5, TILE_SIZE*5//6), 3)  # Pierna izq
            pygame.draw.line(player_surf, (0, 180, 0), (TILE_SIZE*3//5, TILE_SIZE*5//6), (TILE_SIZE*3//5, TILE_SIZE*5//6), 3)  # Pierna der
            # Detalles
            pygame.draw.circle(player_surf, WHITE, (TILE_SIZE*2//5, TILE_SIZE//3), TILE_SIZE//12)  # Ojo izq
            pygame.draw.circle(player_surf, WHITE, (TILE_SIZE*3//5, TILE_SIZE//3), TILE_SIZE//12)  # Ojo der
            self.images['player'] = player_surf
            
            # Enemigo (rojo con forma de fantasma)
            enemy_surf = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
            # Cuerpo
            points = [
                (TILE_SIZE//6, TILE_SIZE//2),
                (TILE_SIZE//6, TILE_SIZE//3),
                (TILE_SIZE//3, TILE_SIZE//6),
                (TILE_SIZE*2//3, TILE_SIZE//6),
                (TILE_SIZE*5//6, TILE_SIZE//3),
                (TILE_SIZE*5//6, TILE_SIZE//2),
                (TILE_SIZE*5//6, TILE_SIZE*2//3),
                (TILE_SIZE*3//4, TILE_SIZE*5//6),
                (TILE_SIZE*2//3, TILE_SIZE*2//3),
                (TILE_SIZE//2, TILE_SIZE*5//6),
                (TILE_SIZE//3, TILE_SIZE*2//3),
                (TILE_SIZE//4, TILE_SIZE*5//6),
                (TILE_SIZE//6, TILE_SIZE*2//3)
            ]
            pygame.draw.polygon(enemy_surf, RED, points)
            # Ojos
            pygame.draw.circle(enemy_surf, WHITE, (TILE_SIZE//3, TILE_SIZE//3), TILE_SIZE//8)  # Ojo izq
            pygame.draw.circle(enemy_surf, WHITE, (TILE_SIZE*2//3, TILE_SIZE//3), TILE_SIZE//8)  # Ojo der
            pygame.draw.circle(enemy_surf, BLACK, (TILE_SIZE//3, TILE_SIZE//3), TILE_SIZE//16)  # Pupila izq
            pygame.draw.circle(enemy_surf, BLACK, (TILE_SIZE*2//3, TILE_SIZE//3), TILE_SIZE//16)  # Pupila der
            self.images['enemy'] = enemy_surf
            
            # Jefe (púrpura, más grande y amenazante)
            boss_surf = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
            # Cuerpo
            pygame.draw.circle(boss_surf, (150, 0, 150), (TILE_SIZE//2, TILE_SIZE//2), TILE_SIZE//2.2)
            # Corona
            points = [
                (TILE_SIZE//4, TILE_SIZE//4),
                (TILE_SIZE//3, TILE_SIZE//8),
                (TILE_SIZE*2//5, TILE_SIZE//4),
                (TILE_SIZE//2, TILE_SIZE//8),
                (TILE_SIZE*3//5, TILE_SIZE//4),
                (TILE_SIZE*2//3, TILE_SIZE//8),
                (TILE_SIZE*3//4, TILE_SIZE//4)
            ]
            pygame.draw.polygon(boss_surf, (200, 180, 0), points)  # Corona dorada
            # Ojos
            pygame.draw.circle(boss_surf, RED, (TILE_SIZE//3, TILE_SIZE*2//5), TILE_SIZE//10)  # Ojo izq
            pygame.draw.circle(boss_surf, RED, (TILE_SIZE*2//3, TILE_SIZE*2//5), TILE_SIZE//10)  # Ojo der
            # Boca
            pygame.draw.arc(boss_surf, WHITE, (TILE_SIZE//3, TILE_SIZE//2, TILE_SIZE//3, TILE_SIZE//4), 0, 3.14, 2)
            self.images['boss'] = boss_surf
            
            # Poción (verde con forma de botella)
            potion_surf = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
            # Botella
            pygame.draw.rect(potion_surf, (0, 100, 0), (TILE_SIZE*3//8, TILE_SIZE//6, TILE_SIZE//4, TILE_SIZE//8))  # Tapón
            pygame.draw.polygon(potion_surf, (0, 180, 0), [
                (TILE_SIZE//3, TILE_SIZE//4), 
                (TILE_SIZE*2//3, TILE_SIZE//4), 
                (TILE_SIZE*2//3, TILE_SIZE*3//4), 
                (TILE_SIZE//2, TILE_SIZE*7//8), 
                (TILE_SIZE//3, TILE_SIZE*3//4)
            ])  # Botella
            # Líquido
            pygame.draw.polygon(potion_surf, (100, 255, 100), [
                (TILE_SIZE//3 + 2, TILE_SIZE//2), 
                (TILE_SIZE*2//3 - 2, TILE_SIZE//2), 
                (TILE_SIZE*2//3 - 2, TILE_SIZE*3//4 - 2), 
                (TILE_SIZE//2, TILE_SIZE*7//8 - 2), 
                (TILE_SIZE//3 + 2, TILE_SIZE*3//4 - 2)
            ])  # Líquido
            # Brillo
            pygame.draw.circle(potion_surf, (200, 255, 200), (TILE_SIZE//2, TILE_SIZE*5//8), TILE_SIZE//12)
            self.images['potion'] = potion_surf
            
            # Poder (azul con forma de rayo)
            power_surf = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
            # Rayo
            pygame.draw.polygon(power_surf, (50, 50, 255), [
                (TILE_SIZE//2, TILE_SIZE//8), 
                (TILE_SIZE*3//4, TILE_SIZE*2//5), 
                (TILE_SIZE*3//5, TILE_SIZE*2//5), 
                (TILE_SIZE*2//3, TILE_SIZE*7//8), 
                (TILE_SIZE*2//5, TILE_SIZE*3//5),
                (TILE_SIZE*2//5, TILE_SIZE*3//5),
                (TILE_SIZE*3//5, TILE_SIZE*3//5),
                (TILE_SIZE//4, TILE_SIZE//3)
            ])
            # Brillo
            pygame.draw.polygon(power_surf, (150, 150, 255), [
                (TILE_SIZE//2, TILE_SIZE//6), 
                (TILE_SIZE*2//3, TILE_SIZE*2//5), 
                (TILE_SIZE//2, TILE_SIZE//2), 
                (TILE_SIZE*3//5, TILE_SIZE*3//4)
            ])
            self.images['power'] = power_surf
            
            # Escaleras (púrpura)
            stairs_surf = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
            # Marco
            pygame.draw.rect(stairs_surf, (100, 0, 100), (TILE_SIZE//8, TILE_SIZE//8, TILE_SIZE*3//4, TILE_SIZE*3//4), 3)
            # Escalones
            for i in range(1, 6):
                y_pos = TILE_SIZE//8 + i * (TILE_SIZE*3//4) // 6
                pygame.draw.line(stairs_surf, (150, 0, 150), 
                               (TILE_SIZE//8, y_pos), 
                               (TILE_SIZE*7//8, y_pos), 2)
            # Barandilla
            pygame.draw.line(stairs_surf, (150, 0, 150), 
                           (TILE_SIZE//3, TILE_SIZE//8), 
                           (TILE_SIZE//3, TILE_SIZE*7//8), 2)
            self.images['stairs'] = stairs_surf
            
            # Pared (gris oscuro con textura de ladrillos)
            wall_surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
            wall_surf.fill(DARK_GRAY)
            # Ladrillos horizontales
            for y in range(0, TILE_SIZE, TILE_SIZE//4):
                pygame.draw.line(wall_surf, BLACK, (0, y), (TILE_SIZE, y), 1)
            # Ladrillos verticales (alternados)
            for i in range(4):
                offset = 0 if i % 2 == 0 else TILE_SIZE//2
                for x in range(offset, TILE_SIZE + offset, TILE_SIZE):
                    pygame.draw.line(wall_surf, BLACK, 
                                   (x, i * TILE_SIZE//4), 
                                   (x, (i+1) * TILE_SIZE//4), 1)
            self.images['wall'] = wall_surf
            
            # Suelo (gris con textura de baldosas)
            floor_surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
            floor_surf.fill(GRAY)
            # Líneas de baldosas
            pygame.draw.line(floor_surf, DARK_GRAY, (0, TILE_SIZE//2), (TILE_SIZE, TILE_SIZE//2), 1)
            pygame.draw.line(floor_surf, DARK_GRAY, (TILE_SIZE//2, 0), (TILE_SIZE//2, TILE_SIZE), 1)
            # Sombras
            pygame.draw.line(floor_surf, (80, 80, 80), (0, 0), (TILE_SIZE//2, TILE_SIZE//2), 1)
            pygame.draw.line(floor_surf, (80, 80, 80), (TILE_SIZE, 0), (TILE_SIZE//2, TILE_SIZE//2), 1)
            pygame.draw.line(floor_surf, (80, 80, 80), (0, TILE_SIZE), (TILE_SIZE//2, TILE_SIZE//2), 1)
            pygame.draw.line(floor_surf, (80, 80, 80), (TILE_SIZE, TILE_SIZE), (TILE_SIZE//2, TILE_SIZE//2), 1)
            self.images['floor'] = floor_surf
    
    def reset(self):
        # Reiniciar el juego
        self.current_floor = 0
        self.game_over = False
        self.victory = False
        
        # Generar el primer nivel
        self.generate_floor()
        
        # Crear jugador
        player_pos = self.get_valid_position()
        # Pasar la imagen del jugador si está disponible
        player_img = self.images.get('player') if self.images else None
        self.player = Player(player_pos[0], player_pos[1], player_img)
        
        # Lista de enemigos
        self.enemies = []
        self.spawn_enemies()
        
        # Posición de las escaleras (mover esto antes de spawn_items)
        self.stairs_pos = self.get_valid_position(exclude=[self.player.rect.topleft])
        
        # Lista de objetos
        self.items = []
        self.spawn_items()
        
        # Iniciar música
        # Comentamos esto para evitar errores con archivos de música
        # pygame.mixer.music.play(-1)
    
    def load_sounds(self):
        # Evitamos cargar sonidos para que el juego funcione sin archivos
        self.sounds = {
            'step': None,
            'attack': None,
            'hurt': None,
            'enemy_death': None,
            'power': None,
            'stairs': None
        }
    
    def generate_floor(self):
        # Generar un nuevo piso
        self.level_map, self.walkable_tiles = self.level_generator.generate_floor(
            self.current_floor
        )
    
    def get_valid_position(self, exclude=None):
        if exclude is None:
            exclude = []
        
        # Obtener una posición válida (en un tile caminable)
        while True:
            pos = self.walkable_tiles[pygame.time.get_ticks() % len(self.walkable_tiles)]
            pixel_pos = (pos[0] * TILE_SIZE, pos[1] * TILE_SIZE)
            
            if pixel_pos not in exclude:
                return pixel_pos
    
    def spawn_enemies(self):
        # Limpiar lista de enemigos
        self.enemies = []
        
        # Determinar número de enemigos según el piso
        enemy_count = 2 + self.current_floor
        
        # Generar enemigos
        for _ in range(enemy_count):
            enemy_pos = self.get_valid_position(
                exclude=[self.player.rect.topleft] + [e.rect.topleft for e in self.enemies]
            )
            
            # En el último piso, añadir un jefe
            if self.current_floor == FLOOR_COUNT - 1 and not self.enemies:
                # Pasar la imagen del jefe si está disponible
                boss_img = self.images.get('boss') if self.images else None
                self.enemies.append(Boss(enemy_pos[0], enemy_pos[1], self.level_map, self.walkable_tiles, boss_img))
            else:
                # Pasar la imagen del enemigo si está disponible
                enemy_img = self.images.get('enemy') if self.images else None
                self.enemies.append(Enemy(enemy_pos[0], enemy_pos[1], self.level_map, self.walkable_tiles, enemy_img))
    
    def spawn_items(self):
        # Limpiar lista de objetos
        self.items = []
        
        # Determinar número de objetos
        item_count = 2 + self.current_floor // 2
        
        # Generar objetos
        for _ in range(item_count):
            item_pos = self.get_valid_position(
                exclude=[self.player.rect.topleft, self.stairs_pos] + 
                        [e.rect.topleft for e in self.enemies] +
                        [i['pos'] for i in self.items]
            )
            
            # Determinar tipo de objeto (poción o poder)
            item_type = "potion" if pygame.time.get_ticks() % 2 == 0 else "power"
            
            self.items.append({
                'type': item_type,
                'pos': item_pos,
                'rect': pygame.Rect(item_pos[0], item_pos[1], TILE_SIZE, TILE_SIZE)
            })
    
    def handle_event(self, event):
        # Manejar eventos del juego
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "menu"
        
        # Pasar eventos al jugador
        self.player.handle_event(event)
        
        return None
    
    def update(self):
        if self.game_over:
            return "game_over"
        
        if self.victory:
            return "victory"
        
        # Actualizar jugador
        self.player.update(self.level_map, self.walkable_tiles)
        
        # Comprobar colisión con escaleras
        stairs_rect = pygame.Rect(self.stairs_pos[0], self.stairs_pos[1], TILE_SIZE, TILE_SIZE)
        if self.player.rect.colliderect(stairs_rect):
            if self.sounds['stairs']:
                self.sounds['stairs'].play()
            self.current_floor += 1
            
            # Si llegamos al último piso y derrotamos al jefe, victoria
            if self.current_floor >= FLOOR_COUNT:
                self.victory = True
                safe_play_music(VICTORY_MUSIC)
                return "victory"
            
            # Generar nuevo piso
            self.generate_floor()
            
            # Reposicionar jugador
            player_pos = self.get_valid_position()
            self.player.rect.x, self.player.rect.y = player_pos
            
            # Generar nuevos enemigos y objetos
            self.spawn_enemies()
            self.spawn_items()
            
            # Reposicionar escaleras
            self.stairs_pos = self.get_valid_position(
                exclude=[self.player.rect.topleft] + 
                        [e.rect.topleft for e in self.enemies]
            )
            
            # Si es el último piso, cambiar música
            if self.current_floor == FLOOR_COUNT - 1:
                safe_play_music(BOSS_MUSIC, -1)
        
        # Actualizar enemigos
        for enemy in self.enemies[:]:
            enemy.update(self.player)
            
            # Comprobar colisión con el jugador
            if enemy.rect.colliderect(self.player.rect) and not self.player.is_invulnerable:
                self.player.take_damage(10)
                if self.sounds['hurt']:
                    self.sounds['hurt'].play()
                
                # Comprobar si el jugador ha muerto
                if self.player.health <= 0:
                    self.game_over = True
                    safe_play_music(GAME_OVER_MUSIC)
                    return "game_over"
            
            # Comprobar si el jugador ataca al enemigo
            if self.player.is_attacking and self.player.attack_rect.colliderect(enemy.rect):
                enemy.take_damage(20)
                if self.sounds['attack']:
                    self.sounds['attack'].play()
                
                # Comprobar si el enemigo ha muerto
                if enemy.health <= 0:
                    self.enemies.remove(enemy)
                    if self.sounds['enemy_death']:
                        self.sounds['enemy_death'].play()
        
        # Comprobar colisión con objetos
        for item in self.items[:]:
            if self.player.rect.colliderect(item['rect']):
                if item['type'] == "potion":
                    self.player.heal(POTION_HEAL)
                elif item['type'] == "power":
                    self.player.activate_power()
                    if self.sounds['power']:
                        self.sounds['power'].play()
                
                self.items.remove(item)
        
        return None
    
    def draw(self):
        # Dibujar el nivel
        for y, row in enumerate(self.level_map):
            for x, tile in enumerate(row):
                if self.images:
                    if tile == 1:  # Pared
                        self.screen.blit(self.images['wall'], (x * TILE_SIZE, y * TILE_SIZE))
                    else:  # Suelo
                        self.screen.blit(self.images['floor'], (x * TILE_SIZE, y * TILE_SIZE))
                else:
                    if tile == 1:  # Pared (fallback)
                        pygame.draw.rect(self.screen, DARK_GRAY, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                    else:  # Suelo (fallback)
                        pygame.draw.rect(self.screen, GRAY, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        
        # Dibujar escaleras
        if self.images:
            self.screen.blit(self.images['stairs'], self.stairs_pos)
        else:
            pygame.draw.rect(self.screen, PURPLE, (self.stairs_pos[0], self.stairs_pos[1], TILE_SIZE, TILE_SIZE))
        
        # Dibujar objetos
        for item in self.items:
            if self.images:
                self.screen.blit(self.images[item['type']], item['pos'])
            else:
                if item['type'] == "potion":
                    pygame.draw.rect(self.screen, GREEN, (item['pos'][0], item['pos'][1], TILE_SIZE, TILE_SIZE))
                else:
                    pygame.draw.rect(self.screen, BLUE, (item['pos'][0], item['pos'][1], TILE_SIZE, TILE_SIZE))
        
        # Dibujar enemigos
        for enemy in self.enemies:
            enemy.draw(self.screen)
        
        # Dibujar jugador
        self.player.draw(self.screen)
        
        # Dibujar HUD
        self.draw_hud()
    
    def draw_hud(self):
        # Dibujar barra de salud
        health_bar_width = 200
        health_percentage = max(0, self.player.health / PLAYER_HEALTH)
        pygame.draw.rect(self.screen, RED, (20, 20, health_bar_width, 20))
        pygame.draw.rect(self.screen, GREEN, (20, 20, health_bar_width * health_percentage, 20))
        pygame.draw.rect(self.screen, WHITE, (20, 20, health_bar_width, 20), 2)
        
        # Mostrar piso actual
        font = pygame.font.SysFont(None, 36)
        floor_text = font.render(f"Piso: {self.current_floor + 1}/{FLOOR_COUNT}", True, WHITE)
        self.screen.blit(floor_text, (SCREEN_WIDTH - floor_text.get_width() - 20, 20))
        
        # Mostrar poderes activos
        if self.player.power_active:
            power_text = font.render(f"Poder: {self.player.power_time:.1f}s", True, BLUE)
            self.screen.blit(power_text, (20, 50)) 