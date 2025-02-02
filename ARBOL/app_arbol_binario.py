class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierda = None
        self.derecha = None

class Arbol:
    # Constructor
    def __init__(self):
        self.raiz = None
    
    # Método para saber si el árbol está vacío
    def vacio(self):
        return self.raiz is None
    
    # Método para insertar un nodo en el árbol
    def insertar(self, valor):
        if self.raiz is None:
            self.raiz = Nodo(valor)
        else:
            self._insertar_recursivo(self.raiz, valor)
    
    # Método auxiliar para insertar
    def _insertar_recursivo(self, nodo, valor):
        if valor < nodo.valor:
            if nodo.izquierda is None:
                nodo.izquierda = Nodo(valor)
            else:
                self._insertar_recursivo(nodo.izquierda, valor)
        else:
            if nodo.derecha is None:
                nodo.derecha = Nodo(valor)
            else:
                self._insertar_recursivo(nodo.derecha, valor)
    
    # Método para buscar un nodo en el árbol
    def buscarNodo(self, valor):
        return self._buscar_preorden(self.raiz, valor)
    
    # Método auxiliar para buscar
    def _buscar_preorden(self, nodo, valor):
        if nodo is None:
            return False
        if nodo.valor == valor:
            return True
        return self._buscar_preorden(nodo.izquierda, valor) or self._buscar_preorden(nodo.derecha, valor)
    
    def imprimirArbol(self, nodo=None, prefijo="", es_izquierda=True):
        if nodo is None:
            nodo = self.raiz
        
        if nodo.derecha:
            self.imprimirArbol(nodo.derecha, prefijo + ("│   " if es_izquierda else "    "), False)
        
        print(prefijo + ("└── " if es_izquierda else "┌── ") + str(nodo.valor))
        
        if nodo.izquierda:
            self.imprimirArbol(nodo.izquierda, prefijo + ("    " if es_izquierda else "│   "), True)

# Ejemplo de uso
arbol = Arbol()
arbol.insertar(10)
arbol.insertar(5)
arbol.insertar(15)
arbol.insertar(3)
arbol.insertar(7)

print("Árbol:")
arbol.imprimirArbol()

print("\n¿Existe 10 en el árbol?:", arbol.buscarNodo(10))
print("¿Existe 20 en el árbol?:", arbol.buscarNodo(20))
