import os
import pygame

# Crear estructura de carpetas
folders = [
    "assets",
    "assets/images",
    "assets/sounds",
    "assets/music"
]

for folder in folders:
    if not os.path.exists(folder):
        os.makedirs(folder)
        print(f"Creada carpeta: {folder}")

# Crear imágenes básicas
pygame.init()

images = {
    "player.svg": (32, 32, (0, 255, 0)),
    "enemy.svg": (32, 32, (255, 0, 0)),
    "boss.svg": (48, 48, (128, 0, 128)),
    "wall.svg": (32, 32, (100, 100, 100)),
    "floor.svg": (32, 32, (200, 200, 200)),
    "stairs.svg": (32, 32, (255, 215, 0)),
    "potion.svg": (32, 32, (0, 255, 0)),
    "power.svg": (32, 32, (0, 0, 255))
}

for name, (width, height, color) in images.items():
    surface = pygame.Surface((width, height))
    surface.fill(color)
    pygame.image.save(surface, f"assets/images/{name}")
    print(f"Creada imagen: assets/images/{name}")

print("¡Configuración completada! Ahora puedes ejecutar el juego.") 