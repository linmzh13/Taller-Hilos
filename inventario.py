from threading import Thread, Barrier, Lock

inventario = 1
ventas_aprobadas = []
barrera = Barrier(2)
candado = Lock()

def vender(caja):
    global inventario

    if inventario > 0:
        decision = True
    else:
        decision = False

    print(f"{caja} consulta inventario: {inventario}")
    print(f"{caja} decision de venta: {decision}")

    barrera.wait()

    if decision:
        inventario -= 1
        ventas_aprobadas.append(caja)
        print(f"{caja}: venta aprobada")


def prueba_sin_lock():
    global inventario, ventas_aprobadas

    inventario = 1
    ventas_aprobadas = []

    print("\n========== VERSION SIN LOCK ==========")

    caja1 = Thread(target=vender, args=("Caja 1",))
    caja2 = Thread(target=vender, args=("Caja 2",))

    caja1.start()
    caja2.start()

    caja1.join()
    caja2.join()

    print("\nResultados sin Lock:")
    print("Ventas aprobadas:", len(ventas_aprobadas))
    print("Inventario final:", inventario)

def vender_seguro(caja):
    global inventario

    with candado:
        print(f"{caja} consulta inventario: {inventario}")

        if inventario > 0:
            inventario -= 1
            ventas_aprobadas.append(caja)
            print(f"{caja}: venta aprobada")
        else:
            print(f"{caja}: venta rechazada")


def prueba_con_lock():
    global inventario, ventas_aprobadas

    inventario = 1
    ventas_aprobadas = []

    print("\n========== VERSION CON LOCK ==========")

    caja1 = Thread(target=vender_seguro, args=("Caja 1",))
    caja2 = Thread(target=vender_seguro, args=("Caja 2",))

    caja1.start()
    caja2.start()

    caja1.join()
    caja2.join()

    print("\nResultados con Lock:")
    print("Ventas aprobadas:", len(ventas_aprobadas))
    print("Inventario final:", inventario)

    assert len(ventas_aprobadas) == 1
    assert inventario == 0

    print("Verificacion correcta: una sola venta aprobada")

if __name__ == "__main__":
    prueba_sin_lock()
    prueba_con_lock()
