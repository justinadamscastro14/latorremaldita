import random
from src.utils.constants import *

class LevelGenerator:
    def __init__(self):
        pass
    
    def generate_floor(self, floor_number):
        """
        Genera un nuevo piso de la torre
        
        Args:
            floor_number: Número del piso actual (0-indexed)
        
        Returns:
            Tupla (level_map, walkable_tiles) donde:
            - level_map es una matriz 2D que representa el mapa (1 = pared, 0 = suelo)
            - walkable_tiles es una lista de tuplas (x, y) con las posiciones de los tiles caminables
        """
        # Determinar tamaño del mapa según el piso
        width = 25 + floor_number * 2
        height = 20 + floor_number * 2
        
        # Crear mapa vacío (todo paredes)
        level_map = [[1 for _ in range(width)] for _ in range(height)]
        
        # Determinar número de habitaciones
        num_rooms = random.randint(MIN_ROOMS, MAX_ROOMS)
        
        # Lista para almacenar las habitaciones
        rooms = []
        
        # Generar habitaciones
        for _ in range(num_rooms):
            # Tamaño aleatorio de la habitación
            room_width = random.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
            room_height = random.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
            
            # Posición aleatoria (asegurando que esté dentro del mapa)
            x = random.randint(1, width - room_width - 1)
            y = random.randint(1, height - room_height - 1)
            
            # Crear la habitación (establecer tiles como suelo)
            for i in range(y, y + room_height):
                for j in range(x, x + room_width):
                    level_map[i][j] = 0
            
            # Guardar la habitación
            rooms.append((x, y, room_width, room_height))
        
        # Conectar habitaciones con pasillos
        for i in range(len(rooms) - 1):
            # Obtener centros de las habitaciones
            x1 = rooms[i][0] + rooms[i][2] // 2
            y1 = rooms[i][1] + rooms[i][3] // 2
            x2 = rooms[i + 1][0] + rooms[i + 1][2] // 2
            y2 = rooms[i + 1][1] + rooms[i + 1][3] // 2
            
            # Crear pasillo horizontal y luego vertical (o viceversa)
            if random.random() < 0.5:
                # Horizontal y luego vertical
                self._create_horizontal_tunnel(level_map, x1, x2, y1)
                self._create_vertical_tunnel(level_map, y1, y2, x2)
            else:
                # Vertical y luego horizontal
                self._create_vertical_tunnel(level_map, y1, y2, x1)
                self._create_horizontal_tunnel(level_map, x1, x2, y2)
        
        # Recopilar tiles caminables
        walkable_tiles = []
        for y in range(height):
            for x in range(width):
                if level_map[y][x] == 0:
                    walkable_tiles.append((x, y))
        
        return level_map, walkable_tiles
    
    def _create_horizontal_tunnel(self, level_map, x1, x2, y):
        """Crea un pasillo horizontal entre x1 y x2 en la fila y"""
        for x in range(min(x1, x2), max(x1, x2) + 1):
            level_map[y][x] = 0
    
    def _create_vertical_tunnel(self, level_map, y1, y2, x):
        """Crea un pasillo vertical entre y1 e y2 en la columna x"""
        for y in range(min(y1, y2), max(y1, y2) + 1):
            level_map[y][x] = 0 