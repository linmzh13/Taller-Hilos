# Taller-Hilos

## Estructura del Proyecto

* **`sensores.py`**: Simulación y medición de tiempos de ejecución para accesos concurrentes a sensores (comparativa entre ejecución secuencial, hilos masivos con `join()` al final, y `join()` secuencial tras cada `start()`)[cite: 8, 10].
* **`inventario.py`**: Simulación de condición de carrera sobre un recurso compartido (inventario de 1 unidad) utilizando `Barrier` sin protección y exclusión mutua mediante `Lock`[cite: 6, 10].
* **`servidor_chat_2.py`**: Servidor de chat TCP multihilo que gestiona conexiones simultáneas, difusión de mensajes y el comando privado `/usuarios` protegido con hilos de seguridad y candados de envío.
* **`cliente_chat_2.py`**: Cliente de chat TCP con recepción asíncrona mediante un hilo secundario (`daemon=True`) mientras la terminal principal interactúa con el usuario vía `input()`[cite: 5, 11].
* **`registro_chat.txt`**: Registro automatizado de prueba que valida la interacción entre múltiples clientes (Ana, Luis y Marta).

---

## 1. Consultas a Sensores (`sensores.py`)

Este ejercicio evalúa el comportamiento temporal al leer tres sensores con tiempos de respuesta independientes ($A = 1.0\text{ s}$, $B = 2.0\text{ s}$, $C = 1.5\text{ s}$)[cite: 8, 10].

### Tabla de Tiempos y Resultados
| Modo de Ejecución | Tiempo Previsto (Teórico) | Mediana Medida |
| :--- | :--- | :--- |
| **Secuencial (llamadas directas)** | $\approx 4.5\text{ s}$ ($1.0 + 2.0 + 1.5$) | *~4.500 s* |
| **Todos los hilos y después esperarlos** | $\approx 2.0\text{ s}$ (el tiempo del sensor más lento: $B$) | *~2.000 s* |
| **Join después de cada start()** | $\approx 4.5\text{ s}$ (bloqueo secuencial forzado) | *~4.500 s* |

### Explicación de los modos de `join()`
* **`join()` al final de todos los `start()`**: Permite el **solapamiento completo (concurrencia real)** de las esperas. Todos los hilos se lanzan casi simultáneamente y el hilo principal espera a que el más lento termine, reduciendo el tiempo total al del proceso máximo ($2.0\text{ s}$).
* **`join()` inmediato tras cada `start()`**: Anula la concurrencia. El hilo principal se bloquea esperando a que el Sensor A termine antes de iniciar el Sensor B, convirtiendo la ejecución efectivamente en **secuencial**.

---

## 2. Dos Cajas, Una Unidad (`inventario.py`)

Se simula un conflicto de acceso concurrente a un recurso crítico (inventario compartido con 1 unidad inicial)[cite: 6, 10].

* **Versión sin Lock:** Utiliza una `Barrier(2)` para sincronizar la lectura de ambas cajas antes de aplicar los descuentos[cite: 6, 10]. Al no haber exclusión mutua, ambas cajas leen `inventario = 1` de forma simultánea, evaluando la decisión como `True` y generando sobreventa o inconsistencias lógicas.
* **Versión con Lock:** Utiliza un objeto `Lock()` que garantiza exclusión mutua estricta. La primera caja en adquirir el candado consulta, descuenta y aprueba la venta, dejando el inventario en `0` para que la segunda caja evalúe el saldo como agotado y rechace la transacción[cite: 6, 10].

### Salida de Ejecución:
```text
========== VERSION SIN LOCK ==========
Caja 1 consulta inventario: 1
Caja 1 decision de venta: True
Caja 2 consulta inventario: 1
Caja 2 decision de venta: True
Caja 1: venta aprobada

Resultados sin Lock:
Ventas aprobadas: 2
Inventario final: 0

========== VERSION CON LOCK ==========
Caja 1 consulta inventario: 1
Caja 1: venta aprobada
Caja 2 consulta inventario: 0
Caja 2: venta rechazada

Resultados con Lock:
Ventas aprobadas: 1
Inventario final: 0
Verificacion correcta: una sola venta aprobada
