def calcular_devolucion(monto):
    # Lista de denominaciones en orden descendente
    denominaciones = [100000, 50000, 20000, 10000, 5000, 2000, 1000, 500, 200, 100, 50]
    resultado = []

    for denominacion in denominaciones:
        cantidad = monto // denominacion  # Cantidad de billetes/monedas de esta denominación
        if cantidad > 0:
            resultado.append((denominacion, cantidad))
            monto -= cantidad * denominacion  # Actualizamos el monto restante

    return resultado

# Ejemplo de uso
monto_a_devolver = 57900
devolucion = calcular_devolucion(monto_a_devolver)
print("Devolución:")
for denom, cant in devolucion:
    print(f"{cant} x ${denom}")
