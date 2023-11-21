import json
from collections import Counter

class heapour:
    def __init__(self):
        self.heap = []

    def push(self, item):
        self.heap.append(item)
        self._sift_up(len(self.heap) - 1)

    def pop(self):
        if len(self.heap) == 0:
            raise IndexError("Pop from empty heap")
        self._swap(0, len(self.heap) - 1)
        item = self.heap.pop()
        self._sift_down(0)
        return item



def contar_frecuencias(texto):
    frecuencias = {}
    for caracter in texto:
        if caracter in frecuencias:
            frecuencias[caracter] += 1
        else:
            frecuencias[caracter] = 1
    return frecuencias



    #FUNCIONES PARA CIFRAR TEXTO
class Nodo:
    def __init__(self, caracter, frecuencia):
        self.caracter = caracter
        self.frecuencia = frecuencia
        self.izquierda = None
        self.derecha = None

    def __lt__(self, otro):
        return self.frecuencia < otro.frecuencia

def crear_arbol_huffman(frecuencia_caracteres):
    heap = heapour()
    for caracter, frecuencia in frecuencia_caracteres.items():
        heap.push(Nodo(caracter, frecuencia))

    while len(heap.heap) > 1:
        nodo_izquierda = heap.pop()
        nodo_derecha = heap.pop()

        nodo_fusionado = Nodo(None, nodo_izquierda.frecuencia + nodo_derecha.frecuencia)
        nodo_fusionado.izquierda = nodo_izquierda
        nodo_fusionado.derecha = nodo_derecha

        heap.push(nodo_fusionado)

    return heap.pop()

def generar_codigos_huffman(nodo, codigo_actual="", codigo_caracteres={}):
    if nodo is None:
        return

    # Si es un nodo hoja, agregamos su código al diccionario
    if nodo.caracter is not None:
        codigo_caracteres[nodo.caracter] = codigo_actual
        return

    generar_codigos_huffman(nodo.izquierda, codigo_actual + "0", codigo_caracteres)
    generar_codigos_huffman(nodo.derecha, codigo_actual + "1", codigo_caracteres)
    
    return codigo_caracteres

def cifrar_texto(texto, arbol_huffman):
    codigos = generar_codigos_huffman(arbol_huffman)
    texto_cifrado = ""
    for caracter in texto:
        texto_cifrado += codigos.get(caracter, "")
    return texto_cifrado


def arbol_a_json(nodo):
    if nodo is None:
        return None
    return {
        'caracter': nodo.caracter,
        'frecuencia': nodo.frecuencia,
        'izq': arbol_a_json(nodo.izquierda),
        'der': arbol_a_json(nodo.derecha)
    }


def guardar_texto_cifrado(texto_cifrado, nombre_archivo):
    with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
        archivo.write(texto_cifrado)


    ######################################################################################################################################


    #FUNCIONES PARA DESCIFRAR TEXTO
    
def reconstruir_arbol(datos_nodo):
    if datos_nodo is None:
        return None

    # Usa .get() para evitar KeyError si la clave no existe
    caracter = datos_nodo.get('caracter')
    frecuencia = datos_nodo.get('frecuencia') # cambio...

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

        # Verificar si nodo_actual es None
        if nodo_actual is None:
            raise ValueError("Secuencia de bits inválida en el texto cifrado")

        if nodo_actual.caracter is not None:
            texto_descifrado += nodo_actual.caracter
            nodo_actual = arbol_huffman
            
    return texto_descifrado





def leer_texto(arch):
    with open(arch, 'r') as archivo:
        datos = json.load(archivo)
    return datos

def leer_archivo_txt(ruta_archivo):
    with open(ruta_archivo, 'r') as archivo:
        contenido = archivo.read()
    return contenido



arch = './arbol_huffman.json'
datos_arbol = leer_texto(arch)
arbol_huffman = reconstruir_arbol(datos_arbol)


ruta_archivo_txt = './texto_cifrado.txt' 
texto_cifrado = leer_archivo_txt(ruta_archivo_txt)

mensaje_descifrado = descifrar_texto(texto_cifrado, arbol_huffman)
print(mensaje_descifrado)


enlace = "https://github.com/Daavvvvvv/Proyecto_Datos2/tree/master"
frecuencias = contar_frecuencias(enlace)
arbol_huffman= crear_arbol_huffman(frecuencias)

datos_arbol_json = arbol_a_json(arbol_huffman)

with open('arbol_huffman.json', 'w', encoding='utf-8') as archivo:
    json.dump(datos_arbol_json, archivo, ensure_ascii=False, indent=4)

cifrado = cifrar_texto(enlace, arbol_huffman)
guardar_texto_cifrado(cifrado, "texto_cifrado.txt")