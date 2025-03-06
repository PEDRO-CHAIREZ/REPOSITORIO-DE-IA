class Nodo:
    def __init__(self, nombre):
        self.nombre = nombre
        self.izquierda = None
        self.derecha = None

class Arbol:
    def __init__(self):
        self.raiz = None

    # Método para verificar si el árbol está vacío
    def esta_vacio(self):
        return self.raiz is None

    # Método para insertar un nodo en el árbol
    def insertar(self, nombre):
        self.raiz = self._insertar_recursivo(self.raiz, nombre)

    def _insertar_recursivo(self, nodo_actual, nombre):
        if nodo_actual is None:
            return Nodo(nombre)

        if nombre < nodo_actual.nombre:
            nodo_actual.izquierda = self._insertar_recursivo(nodo_actual.izquierda, nombre)
        elif nombre > nodo_actual.nombre:
            nodo_actual.derecha = self._insertar_recursivo(nodo_actual.derecha, nombre)

        return nodo_actual

    # Método para buscar un nodo en el árbol
    def buscar_nodo(self, nombre):
        return self._buscar_recursivo(self.raiz, nombre)

    def _buscar_recursivo(self, nodo_actual, nombre):
        if nodo_actual is None:
            return False

        if nombre == nodo_actual.nombre:
            return True

        if nombre < nodo_actual.nombre:
            return self._buscar_recursivo(nodo_actual.izquierda, nombre)
        else:
            return self._buscar_recursivo(nodo_actual.derecha, nombre)

    # Método para imprimir el árbol en orden (in-order traversal)
    def imprimir_arbol(self):
        self._imprimir_in_orden(self.raiz)

    def _imprimir_in_orden(self, nodo_actual):
        if nodo_actual is not None:
            self._imprimir_in_orden(nodo_actual.izquierda)
            print(nodo_actual.nombre)
            self._imprimir_in_orden(nodo_actual.derecha)

# Método principal (main) para probar el árbol
if __name__ == "__main__":
    arbol = Arbol()

    arbol.insertar("Juan")
    arbol.insertar("Ana")
    arbol.insertar("Pedro")
    arbol.insertar("Luis")

    print("Árbol en orden:")
    arbol.imprimir_arbol()

    print("\nBuscando 'Ana':", arbol.buscar_nodo("Ana"))
    print("Buscando 'Carlos':", arbol.buscar_nodo("Carlos"))