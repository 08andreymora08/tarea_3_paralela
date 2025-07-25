#!/usr/bin/env python3
"""
Parte A: Operaciones colectivas en MPI para calcular
mínimo, máximo y promedio global de un arreglo de N valores.
"""

from mpi4py import MPI
import numpy as np
import sys

def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    # argumento: tamaño total N
    if rank == 0:
        if len(sys.argv) != 2:
            print(f"Uso: mpirun -np <p> python {sys.argv[0]} <N_total>")
            comm.Abort(1)
        N = int(sys.argv[1])
        if N % size != 0:
            print("Error: N debe ser divisible entre número de procesos.")
            comm.Abort(1)
        data = np.random.random_sample(N) * 100.0
    else:
        N = None
        data = None

    # enviar N a todos
    N = comm.bcast(N, root=0)

    # repartir partes iguales
    chunk_size = N // size
    local = np.empty(chunk_size, dtype='d')
    comm.Scatter(data, local, root=0)

    # estadística local
    local_min = np.min(local)
    local_max = np.max(local)
    local_sum = np.sum(local)

    # reducciones globales
    global_min = comm.reduce(local_min, op=MPI.MIN, root=0)
    global_max = comm.reduce(local_max, op=MPI.MAX, root=0)
    total_sum  = comm.reduce(local_sum,  op=MPI.SUM, root=0)

    if rank == 0:
        global_avg = total_sum / N
        print(f"Resultado global (N={N}):")
        print(f"  Mínimo : {global_min:.4f}")
        print(f"  Máximo : {global_max:.4f}")
        print(f"  Promedio: {global_avg:.4f}")

if __name__ == "__main__":
    main()
