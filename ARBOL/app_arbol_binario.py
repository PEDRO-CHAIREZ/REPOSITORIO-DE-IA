class Nodo:
    def __init__(self, nombre):
        self.nombre = nombre
        self.padre = None
        self.izquierda = None
        self.derecha = None
        self.es_raiz = False

class Arbol:
    def __init__(self):
        self.raiz = None

    def vacio(self):
        # Retorna True si el árbol está vacío
        return self.raiz == None

    def buscarNodo(self, nombre):
        """
        Busca recursivamente un nodo con el nombre dado.
        Retorna el nodo si se encuentra; de lo contrario, retorna None.
        """
        return self._buscarNodo(self.raiz, nombre)

    def _buscarNodo(self, nodo, nombre):
        if nodo is None:
            return None
        if nodo.nombre == nombre:
            return nodo
        # Se busca en el subárbol izquierdo
        nodo_encontrado = self._buscarNodo(nodo.izquierda, nombre)
        if nodo_encontrado is None:
            # Si no se encontró en el izquierdo, se busca en el derecho
            nodo_encontrado = self._buscarNodo(nodo.derecha, nombre)
        return nodo_encontrado

    def insertar(self, nombre):
        """
        Inserta un nuevo nodo con el nombre especificado.
        Si el árbol está vacío, el nuevo nodo se convierte en la raíz.
        De lo contrario, se inserta siguiendo la propiedad del árbol de búsqueda binario.
        """
        nuevo_nodo = Nodo(nombre)
        if self.vacio():
            self.raiz = nuevo_nodo
        else:
            self._insertar(self.raiz, nuevo_nodo)

    def _insertar(self, actual, nuevo_nodo):
        if nuevo_nodo.nombre < actual.nombre:
            if actual.izquierda is None:
                actual.izquierda = nuevo_nodo
            else:
                self._insertar(actual.izquierda, nuevo_nodo)
        else:
            if actual.derecha is None:
                actual.derecha = nuevo_nodo
            else:
                self._insertar(actual.derecha, nuevo_nodo)

    def imprimirArbol(self):
        """Imprime el árbol de forma visual."""
        self._imprimirArbol(self.raiz, 0)

    def _imprimirArbol(self, nodo, nivel):
        if nodo is not None:
            self._imprimirArbol(nodo.derecha, nivel + 1)
            print('    ' * nivel + f'-> {nodo.nombre}')
            self._imprimirArbol(nodo.izquierda, nivel + 1)

