#!/usr/bin/env python3
"""
Medición de latencia y ancho de banda para distintos tamaños de mensaje:
1 byte, 1 kilobyte y 1 megabyte.

Genera un gráfico (log–log) de RTT promedio vs. tamaño de mensaje.
"""

from mpi4py import MPI
import numpy as np
import sys
import matplotlib.pyplot as plt

def measure_rtt(iterations, msg_size, comm):
    rank = comm.Get_rank()
    buf = bytearray(msg_size)
    comm.Barrier()  # sincronizar antes de medir

    if rank == 0:
        t0 = MPI.Wtime()
        for _ in range(iterations):
            comm.Send([buf, MPI.BYTE], dest=1, tag=0)
            comm.Recv([buf, MPI.BYTE], source=1, tag=0)
        t1 = MPI.Wtime()
        return (t1 - t0) / iterations
    else:
        for _ in range(iterations):
            comm.Recv([buf, MPI.BYTE], source=0, tag=0)
            comm.Send([buf, MPI.BYTE], dest=0, tag=0)
        return None

def main():
    comm = MPI.COMM_WORLD
    size = comm.Get_size()
    rank = comm.Get_rank()

    if size != 2:
        if rank == 0:
            print("Error: ejecutar con 2 procesos: mpirun -np 2 python3 medidor_latencia.py")
        sys.exit(1)

    # configuración de tamaños e iteraciones
    tests = [
        (1,    10000),   # 1 byte
        (1024,  5000),   # 1 KB
        (1024*1024, 500) # 1 MB
    ]

    resultados = []
    for msg_size, iters in tests:
        rtt = measure_rtt(iters, msg_size, comm)
        if rank == 0:
            resultados.append((msg_size, iters, rtt))

    if rank == 0:
        # preparar datos para graficar
        tamaños = [r[0] for r in resultados]
        rtts_us = [r[2]*1e6 for r in resultados]  # convertir a µs

        # imprimir tabla de resultados
        print("\nResultados de latencia:")
        print(" Tamaño  Iteracion  Latencia promedio por mensaje(microsegundos)   Latencia estimada unidireccional(microsegundos)")
        for msg_size, iters, rtt in resultados:
            rtt_us = rtt*1e6
            one_way = rtt_us/2
            print(f"{msg_size:8d}  {iters:5d}    {rtt_us:10.2f}          {one_way:10.2f}")

        # graficar
        plt.figure()
        plt.xscale('log')
        plt.yscale('log')
        plt.plot(tamaños, rtts_us, marker='o')
        plt.xlabel('Tamaño de mensaje (bytes)')
        plt.ylabel('RTT promedio (µs)')
        plt.title('RTT vs. tamaño de mensaje (log–log)')
        plt.grid(True, which='both', ls='--', lw=0.5)
        plt.tight_layout()
        plt.savefig('latencia_vs_tamano.png')
        print("\nGráfico guardado en 'latencia_vs_tamano.png'.")

if __name__ == "__main__":
    main()
