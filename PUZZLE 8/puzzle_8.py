import heapq # Librería para manejar colas de prioridad
import time # Librería para medir el tiempo de la ejecución

class Puzzle:
    # Constructor de la clase Puzzle
    def __init__(self, board, moves=0, previous=None):
        self.board = board
        self.moves = moves
        self.previous = previous
        self.zero_pos = self.find_zero()

    # Método para encontrar la posición del 0 en el tablero
    def find_zero(self):
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 0:
                    return i, j
                
     # Método para comparar el resultado de dos instancias            
    def __lt__(self, other):
        return (self.moves + self.heuristic()) < (other.moves + other.heuristic())
    
     # Método para calcular la heurística de cada instancia
    def heuristic(self):
        # Objetivo/meta final
        goal = {1: (0, 0), 2: (0, 1), 3: (0, 2),
                4: (1, 0), 5: (1, 1), 6: (1, 2),
                7: (2, 0), 8: (2, 1), 0: (2, 2)}
        # Suma de las distancias Manhattan de cada número a su posición final
        return sum(abs(i - goal[val][0]) + abs(j - goal[val][1])
                   for i, row in enumerate(self.board)
                   for j, val in enumerate(row) if val) 
    
    # Método para obtener todos los posibles movimientos
    def possible_moves(self):
        x, y = self.zero_pos
        moves = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)] #Arriba, abajo, izquierda, derecha
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 3 and 0 <= ny < 3:
                new_board = [list(row) for row in self.board]
                # Intercambio de posiciones para obtener un nuevo tablero
                new_board[x][y], new_board[nx][ny] = new_board[nx][ny], new_board[x][y]
                moves.append(Puzzle(new_board, self.moves + 1, self))
        
        return moves
    # Método para reconstruir el camino de la solución
    def reconstruct_path(self):
        path = []
        node = self
        while node:
            path.append(node.board)
            node = node.previous
        return path[::-1]
    

# Método para resolver el puzzle
def solve_puzzle(start_board):
    start_time = time.time() # Aqui se toma el tiempo inicial
    start = Puzzle(start_board)
    heap = [start] # Se crea la cola
    visited = set() # Conjunto de nodos visitados
    
    # Mientras haya nodos en la cola se sigue buscando
    while heap:
        current = heapq.heappop(heap)
        if current.heuristic() == 0: # Si la heurística es 0, se ha llegado a la solución
            end_time = time.time() # Se toma el tiempo final
            return current.reconstruct_path(), current.moves, end_time - start_time
        
        visited.add(tuple(tuple(row) for row in current.board)) # Se añade el nodo actual a los visitados
        
        # Se añaden los posibles movimientos a la cola si no han sido visitados
        for move in current.possible_moves(): 
            if tuple(tuple(row) for row in move.board) not in visited:
                heapq.heappush(heap, move)
    
    end_time = time.time()
    return None, 0, end_time - start_time # Si no hay solución, se retorna nulo y el tiempo

if __name__ == "__main__":
    # Tablero de inicio
    start_board = [[1, 5, 3],
                   [6, 0, 4],
                   [7, 2, 8]]
    
    solution, moves, duration = solve_puzzle(start_board)
    if solution:
        for step in solution: # Se imprime cada paso de la solución
            for row in step:
                print(row)
            print()
        print(f"Número total de movimientos: {moves}")
        print(f"Tiempo de resolución: {duration:.4f} segundos")
    else:
        print("No hay solución")
        print(f"Tiempo transcurrido: {duration:.4f} segundos")

    #EJEMPLO SIN SOLUCION
#[[1, 2, 3],[4, 5, 6],[8, 7, 0]]