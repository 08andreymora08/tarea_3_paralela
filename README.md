# Tarea 3:

## Dependencias
- Python 3.7 o superior  
- mpi4py (`pip install mpi4py`)  
- numpy (`pip install numpy`)  
- matplotlib (`pip install matplotlib`)  

## Cómo usar

1. **Parte A (estadisticas_mpi.py)**  
   ```bash
   mpirun -np 4 python3 estadisticas_mpi.py 1000000
   ````

* Crea 1 000 000 de números aleatorios.
* Calcula el mínimo, el máximo y el promedio.
* El número total (1000000) debe dividirse igual entre los 4 procesos.

2. **Parte B (latencia\_mpi.py)**

   ```bash
   mpirun -np 2 python3 latencia_mpi.py 10000 1
   ```

   * Envía un mensaje de 1 byte 10 000 veces de ida y vuelta.
   * Muestra el tiempo promedio total (RTT) y el tiempo de ida (RTT/2).

3. **Parte opcional (medidor\_latencia.py)**

   ```bash
   mpirun -np 2 python3 medidor_latencia.py
   ```

   * Prueba con mensajes de 1 B, 1 KB y 1 MB.
   * Guarda una tabla en pantalla y un gráfico `latencia_vs_tamano.png`.

---

## Resultados

| Tamaño | Iter. | RTT prom. (µs) | Latencia ida (µs) |
| -----: | ----: | -------------: | ----------------: |
| 1 byte | 10000 |           3.78 |              1.89 |
|   1 KB |  5000 |           4.05 |              2.02 |
|   1 MB |   500 |         224.81 |            112.41 |

---

## Qué vemos

* **Mensajes pequeños (1 B, 1 KB):**
  El tiempo es casi el mismo (3–4 µs) porque lo que más pesa es el “trabajo extra” de MPI y el manejo en memoria.

* **Mensaje grande (1 MB):**
  El tiempo sube mucho (≈225 µs) porque ahora pesa el envío de muchos datos.

* En el gráfico de ejes log–log se aprecia que:

  * Para tamaños pequeños la línea es casi plana.
  * Para tamaños grandes la línea sube en proporción al tamaño.

---

## Por qué varía el tiempo

1. La pc puede estar ocupado con otros programas.
2. MPI usa distintos métodos internos para mandar datos.
3. Si hay más procesos que núcleos, el sistema tarda más.