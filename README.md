# Taller Hilos
## Integrantes: Lineth Paola Márquez Hernández y Jair Santiago Garzón Arias.

## Estructura del Proyecto

* `sensores.py`: Simulación de lectura de 3 sensores para comparar tiempos entre ejecución secuencial y distintos usos de hilos (`start()` y `join()`).
* `inventario.py`: Demostración de una condición de carrera (*race condition*) en un sistema de ventas con dos cajas y su solución usando `Lock`.
* `servidor_chat.py` y `cliente_chat.py`: Chat TCP multicliente donde se implementó el comando `/usuarios` protegiendo los recursos compartidos.
* `registro_chat.txt`: Evidencia de la ejecución y pruebas realizadas en las terminales del chat.
* `INFORME.md`: Documento con los resultados obtenidos, análisis y respuestas a las preguntas de la guía.

---

## Cómo ejecutar cada archivo

Todos los scripts usan únicamente la biblioteca estándar de Python 3.

### 1. Simulación de Sensores
Ejecuta el script para correr las 3 repeticiones de cada modo y ver el cálculo automático de la mediana:
```bash
python sensores.py
```

### 2. Control de Inventario (Cajas)
Ejecuta el script para ver primero el fallo sin sincronización (ventas duplicadas e inventario negativo) y luego la ejecución segura con `Lock`:
```bash
python inventario.py
```

### 3. Chat TCP con comando `/usuarios`
Para probar el chat necesitas abrir **4 terminales** distintas:

1. **Terminal 1 (Servidor):**
   ```bash
   python servidor_chat.py
   ```
2. **Terminales 2, 3 y 4 (Clientes - ej. Ana, Luis y Marta):**
   ```bash
   python cliente_chat.py
   ```
   *Escribe el nombre de usuario al conectar. Luego puedes chatear normalmente, usar `/usuarios` para ver quién está en línea o `/salir` para desconectarte.*
