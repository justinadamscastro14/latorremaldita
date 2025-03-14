# Constantes del juego

# Configuración de pantalla
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TITLE = "La Torre Maldita"
FPS = 60

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (100, 100, 100)
DARK_GRAY = (50, 50, 50)
PURPLE = (128, 0, 128)

# Jugador
PLAYER_SPEED = 5
PLAYER_SIZE = 32
PLAYER_HEALTH = 100

# Enemigos
ENEMY_SPEED = 3
ENEMY_SIZE = 32
ENEMY_DETECTION_RADIUS = 150
ENEMY_PATROL_RADIUS = 100

# Nivel
TILE_SIZE = 32
FLOOR_COUNT = 5  # Número de pisos en la torre
ROOM_MIN_SIZE = 5
ROOM_MAX_SIZE = 10
MIN_ROOMS = 3
MAX_ROOMS = 8

# Objetos
POTION_HEAL = 25
POWER_DURATION = 10  # Duración de poderes en segundos

# Rutas de archivos
ASSETS_DIR = "assets"
IMAGES_DIR = f"{ASSETS_DIR}/images"
SOUNDS_DIR = f"{ASSETS_DIR}/sounds"
MUSIC_DIR = f"{ASSETS_DIR}/music"

# Imágenes
PLAYER_IMG = f"{IMAGES_DIR}/player.svg"
ENEMY_IMG = f"{IMAGES_DIR}/enemy.svg"
BOSS_IMG = f"{IMAGES_DIR}/boss.svg"
WALL_IMG = f"{IMAGES_DIR}/wall.svg"
FLOOR_IMG = f"{IMAGES_DIR}/floor.svg"
STAIRS_IMG = f"{IMAGES_DIR}/stairs.svg"
POTION_IMG = f"{IMAGES_DIR}/potion.svg"
POWER_IMG = f"{IMAGES_DIR}/power.svg"

# Sonidos
STEP_SOUND = f"{SOUNDS_DIR}/step.wav"
ATTACK_SOUND = f"{SOUNDS_DIR}/attack.wav"
HURT_SOUND = f"{SOUNDS_DIR}/hurt.wav"
ENEMY_DEATH_SOUND = f"{SOUNDS_DIR}/enemy_death.wav"
POWER_SOUND = f"{SOUNDS_DIR}/power.wav"
STAIRS_SOUND = f"{SOUNDS_DIR}/stairs.wav"

# Música
MENU_MUSIC = f"{MUSIC_DIR}/menu.mp3"
GAME_MUSIC = f"{MUSIC_DIR}/game.mp3"
BOSS_MUSIC = f"{MUSIC_DIR}/boss.mp3"
VICTORY_MUSIC = f"{MUSIC_DIR}/victory.mp3"
GAME_OVER_MUSIC = f"{MUSIC_DIR}/game_over.mp3" 