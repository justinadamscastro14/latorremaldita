import heapq
from src.utils.constants import *

def astar(start, goal, grid):
    """
    Implementación del algoritmo A* para encontrar el camino más corto entre dos puntos
    
    Args:
        start: Tupla (x, y) con la posición inicial en coordenadas de tile
        goal: Tupla (x, y) con la posición objetivo en coordenadas de tile
        grid: Matriz 2D que representa el mapa (1 = pared, 0 = suelo)
    
    Returns:
        Lista de tuplas (x, y) que representan el camino desde start hasta goal,
        o None si no se encuentra un camino
    """
    # Conjunto de nodos abiertos y cerrados
    open_set = []
    closed_set = set()
    
    # Diccionarios para almacenar el costo g y el padre de cada nodo
    g_score = {start: 0}
    parent = {}
    
    # Función heurística (distancia Manhattan)
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    # Agregar el nodo inicial al conjunto abierto
    heapq.heappush(open_set, (0, start))
    
    while open_set:
        # Obtener el nodo con menor f_score
        _, current = heapq.heappop(open_set)
        
        # Si llegamos al objetivo, reconstruir el camino
        if current == goal:
            path = []
            while current in parent:
                path.append(current)
                current = parent[current]
            return path[::-1]  # Invertir el camino para que vaya desde start hasta goal
        
        # Agregar el nodo actual al conjunto cerrado
        closed_set.add(current)
        
        # Explorar vecinos
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:  # 4 direcciones: abajo, derecha, arriba, izquierda
            neighbor = (current[0] + dx, current[1] + dy)
            
            # Comprobar si el vecino está dentro de los límites del mapa
            if (0 <= neighbor[1] < len(grid) and 
                0 <= neighbor[0] < len(grid[0])):
                
                # Comprobar si el vecino es una pared
                if grid[neighbor[1]][neighbor[0]] == 1:
                    continue
                
                # Comprobar si el vecino ya está en el conjunto cerrado
                if neighbor in closed_set:
                    continue
                
                # Calcular el costo g tentativo
                tentative_g = g_score[current] + 1
                
                # Comprobar si el vecino ya está en el conjunto abierto
                in_open_set = False
                for _, node in open_set:
                    if node == neighbor:
                        in_open_set = True
                        break
                
                # Si el vecino no está en el conjunto abierto o el nuevo camino es mejor
                if not in_open_set or tentative_g < g_score.get(neighbor, float('inf')):
                    # Este camino es mejor, guardar
                    parent[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score = tentative_g + heuristic(neighbor, goal)
                    
                    # Agregar o actualizar el vecino en el conjunto abierto
                    if not in_open_set:
                        heapq.heappush(open_set, (f_score, neighbor))
    
    # No se encontró un camino
    return None 