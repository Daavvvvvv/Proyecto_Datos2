import heapq
import json

class Nodo:
    def __init__(self, caracter, frecuencia):
        self.caracter = caracter
        self.frecuencia = frecuencia
        self.izquierda = None
        self.derecha = None

    # Definimos una comparación para que heapq pueda ordenar los nodos
    def __lt__(self, otro):
        return self.frecuencia < otro.frecuencia

def crear_arbol_huffman(frecuencia_caracteres):
    heap = []
    for caracter, frecuencia in frecuencia_caracteres.items():
        heapq.heappush(heap, Nodo(caracter, frecuencia))

    while len(heap) > 1:
        nodo_izquierda = heapq.heappop(heap)
        nodo_derecha = heapq.heappop(heap)

        nodo_fusionado = Nodo(None, nodo_izquierda.frecuencia + nodo_derecha.frecuencia)
        nodo_fusionado.izquierda = nodo_izquierda
        nodo_fusionado.derecha = nodo_derecha

        heapq.heappush(heap, nodo_fusionado)

    return heap[0]  # Retorna la raíz del árbol de Huffma

def generar_codigos_huffman(nodo, codigo_actual="", codigo_caracteres={}):
    if nodo is None:
        return

    # Si es un nodo hoja, agregamos su código al diccionario
    if nodo.caracter is not None:
        codigo_caracteres[nodo.caracter] = codigo_actual
        return

    generar_codigos_huffman(nodo.izquierda, codigo_actual + "0", codigo_caracteres)
    generar_codigos_huffman(nodo.derecha, codigo_actual + "1", codigo_caracteres)

def cifrar_texto(texto, arbol_huffman):
    codigos = {}
    generar_codigos_huffman(arbol_huffman, "", codigos)

    texto_cifrado = ""
    for caracter in texto:
        texto_cifrado += codigos.get(caracter, "")

    return texto_cifrado

def reconstruir_arbol(datos_nodo):
    if datos_nodo is None:
        return None

    # Usa .get() para evitar KeyError si la clave no existe
    caracter = datos_nodo.get('caracter')
    frecuencia = datos_nodo['frecuencia']

    nodo = Nodo(caracter, frecuencia)

    # Usa las claves 'izq' y 'der' para los nodos hijos
    nodo.izquierda = reconstruir_arbol(datos_nodo.get('izq'))
    nodo.derecha = reconstruir_arbol(datos_nodo.get('der'))

    return nodo


def descifrar_texto(texto_cifrado, arbol_huffman):
    texto_descifrado = ""
    nodo_actual = arbol_huffman

    for bit in texto_cifrado:
        if bit == '0':
            nodo_actual = nodo_actual.izquierda
        else:
            nodo_actual = nodo_actual.derecha

        if nodo_actual.caracter is not None:
            texto_descifrado += nodo_actual.caracter
            nodo_actual = arbol_huffman

    return texto_descifrado


def recorrer_arbol_preorden(nodo, profundidad=0):
    if nodo is not None:
        # Imprime el carácter y la frecuencia de cada nodo
        print("  " * profundidad + f"Carácter: {nodo.caracter}, Frecuencia: {nodo.frecuencia}")
        
        # Recorre el subárbol izquierdo y luego el derecho
        recorrer_arbol_preorden(nodo.izquierda, profundidad + 1)
        recorrer_arbol_preorden(nodo.derecha, profundidad + 1)



def leer_texto(arch):
    with open(arch, 'r') as archivo:
        datos = json.load(archivo)
    return datos

def leer_archivo_txt(ruta_archivo):
    with open(ruta_archivo, 'r') as archivo:
        contenido = archivo.read()
    return contenido



arch = './arbol_huffman_actividad_1.json'
datos_arbol = leer_texto(arch)
arbol_huffman = reconstruir_arbol(datos_arbol)
recorrer_arbol_preorden(arbol_huffman)


ruta_archivo_txt = './texto_actividad_1.txt' 
texto_cifrado = leer_archivo_txt(ruta_archivo_txt)

mensaje_descifrado = descifrar_texto(texto_cifrado, arbol_huffman)
print(mensaje_descifrado)