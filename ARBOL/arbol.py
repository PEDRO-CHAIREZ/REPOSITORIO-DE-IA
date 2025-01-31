class Arbol:
    def __init__(self):
        self.raiz = None

    def vacio(self):
        """Verifica si el árbol está vacío"""
        return self.raiz is None

    def insertar(self, valor):
        """Inserta un nuevo valor en el árbol"""
        self.raiz = self._insertar_recursivo(self.raiz, valor)

    def _insertar_recursivo(self, nodo, valor):
        if nodo is None:
            return Nodo(valor)
        
        if valor < nodo.valor:
            nodo.izquierda = self._insertar_recursivo(nodo.izquierda, valor)
        elif valor > nodo.valor:
            nodo.derecha = self._insertar_recursivo(nodo.derecha, valor)

        return nodo

    def buscarNodo(self, nombre):
        """Busca un nodo en el árbol por su valor"""
        return self._buscarNodo_recursivo(self.raiz, nombre)

    def _buscarNodo_recursivo(self, nodo, nombre):
        if nodo is None or nodo.valor == nombre:
            return nodo
        
        if nombre < nodo.valor:
            return self._buscarNodo_recursivo(nodo.izquierda, nombre)
        else:
            return self._buscarNodo_recursivo(nodo.derecha, nombre)

    def recorridoEnOrden(self):
        """Imprime los valores del árbol en orden"""
        self._recorridoEnOrden_recursivo(self.raiz)
        print()  # Para salto de línea

    def _recorridoEnOrden_recursivo(self, nodo):
        if nodo is not None:
            self._recorridoEnOrden_recursivo(nodo.izquierda)
            print(nodo.valor, end=" ")
            self._recorridoEnOrden_recursivo(nodo.derecha)