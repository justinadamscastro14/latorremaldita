# Implementación del Árbol de Comportamiento

class BTNode:
    """Clase base para todos los nodos del árbol de comportamiento"""
    def run(self, enemy, player):
        """Ejecuta el nodo y devuelve True si tiene éxito, False en caso contrario"""
        pass

class Selector(BTNode):
    """
    Selector (OR lógico): devuelve True si alguno de sus hijos devuelve True,
    False solo si todos sus hijos devuelven False
    """
    def __init__(self, children):
        self.children = children
    
    def run(self, enemy, player):
        for child in self.children:
            if child.run(enemy, player):
                return True
        return False

class Sequence(BTNode):
    """
    Secuencia (AND lógico): devuelve True solo si todos sus hijos devuelven True,
    False si alguno de sus hijos devuelve False
    """
    def __init__(self, children):
        self.children = children
    
    def run(self, enemy, player):
        for child in self.children:
            if not child.run(enemy, player):
                return False
        return True

class Inverter(BTNode):
    """Invierte el resultado de su hijo"""
    def __init__(self, child):
        self.child = child
    
    def run(self, enemy, player):
        return not self.child.run(enemy, player)

# Nodos de acción específicos para el juego

class DetectPlayer(BTNode):
    """Comprueba si el enemigo puede ver al jugador"""
    def run(self, enemy, player):
        if enemy.can_see_player(player):
            enemy.state = "chase"
            return True
        return False

class ChasePlayer(BTNode):
    """Persigue al jugador usando A*"""
    def run(self, enemy, player):
        if enemy.state == "chase":
            enemy.chase_player(player)
            return True
        return False

class Patrol(BTNode):
    """Realiza un patrullaje aleatorio"""
    def run(self, enemy, player):
        enemy.state = "patrol"
        enemy.patrol()
        return True 