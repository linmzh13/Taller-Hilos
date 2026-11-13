from threading import Thread
from time import perf_counter, sleep

def leer_sensor(nombre, espera, inicio):
    tiempo_inicio = perf_counter() - inicio
    print(f"[{tiempo_inicio:.2f} s] {nombre} inicia", flush=True)

    sleep(espera)

    tiempo_fin = perf_counter() - inicio
    print(f"[{tiempo_fin:.2f} s] {nombre} termina", flush=True)


def medir_secuencial(sensores):
    print("\n=== Lectura secuencial ===")
    inicio = perf_counter()

    for sensor in sensores:
        leer_sensor(*sensor, inicio)

    return perf_counter() - inicio


def medir_multihilo(sensores):
    print("\n=== Todos los hilos y después esperarlos ===")
    inicio = perf_counter()

    hilos = [
        Thread(target=leer_sensor, args=(*sensor, inicio))
        for sensor in sensores
    ]

    for hilo in hilos:
        hilo.start()

    for hilo in hilos:
        hilo.join()

    return perf_counter() - inicio


def medir_join_individual(sensores):
    print("\n=== Join después de cada start ===")
    inicio = perf_counter()

    for sensor in sensores:
        hilo = Thread(target=leer_sensor, args=(*sensor, inicio))
        hilo.start()
        hilo.join()

    return perf_counter() - inicio


def main():
    sensores = (
        ("Sensor A", 1.0),
        ("Sensor B", 2.0),
        ("Sensor C", 1.5)
    )

    resultados = [[], [], []]

    for prueba in range(3):
        print(f"\n========== PRUEBA {prueba + 1} ==========")

        resultados[0].append(medir_secuencial(sensores))
        resultados[1].append(medir_multihilo(sensores))
        resultados[2].append(medir_join_individual(sensores))

    print("\n========== RESULTADOS FINALES ==========")

    nombres = [
        "Secuencial",
        "Todos los hilos y después esperarlos",
        "Join después de cada start"
    ]

    for nombre, tiempos in zip(nombres, resultados):
        mediana = sorted(tiempos)[1]
        print(f"{nombre}: {mediana:.3f} segundos")


if __name__ == "__main__":
    main()
