import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  
import csv
import ast  

def graficar_sistema_ecuaciones(A, B):
    n = len(B)
    
    if n == 2:
        # Sistema 2x2 (rectas en el plano)
        x_vals = np.linspace(-5, 5, 100)
        y_vals = []
        for i in range(2):
            y_vals.append((B[i] - A[i, 0]*x_vals) / A[i, 1])
            plt.plot(x_vals, y_vals[i], label=f'Ecuación {i+1}: {A[i, 0]}x + {A[i, 1]}y = {B[i]}')
        
        # Calcular el punto de intersección
        x_interseccion = np.linalg.solve(A, B)
        print(f"Punto de intersección de las rectas: ({x_interseccion[0]:.2f}, {x_interseccion[1]:.2f})")
        
        plt.plot(x_interseccion[0], x_interseccion[1], 'ro', label='Intersección')
        
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('Sistema de Ecuaciones 2x2')
        plt.legend()
        plt.grid(True)
        plt.show()

    elif n == 3:
        # Sistema 3x3 (planos en el espacio)
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        xx, yy = np.meshgrid(np.linspace(-5, 5, 10), np.linspace(-5, 5, 10))

        z_vals = []
        for i in range(3):
            z_vals.append((B[i] - A[i, 0]*xx - A[i, 1]*yy) / A[i, 2])
            ax.plot_surface(xx, yy, z_vals[i], alpha=0.5, label=f'Plano {i+1}: {A[i, 0]}x + {A[i, 1]}y + {A[i, 2]}z = {B[i]}')

        # Calcular el punto de intersección
        punto_interseccion = np.linalg.solve(A, B)
        print(f"Punto de intersección de los planos: ({punto_interseccion[0]:.2f}, {punto_interseccion[1]:.2f}, {punto_interseccion[2]:.2f})")
        
        ax.scatter(punto_interseccion[0], punto_interseccion[1], punto_interseccion[2], color='red', label='Intersección', s=100)

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title('Sistema de Ecuaciones 3x3')
        ax.legend()
        plt.show()

    else:
        raise ValueError("La función graficar_sistema_ecuaciones solo admite sistemas 2x2 o 3x3.")

# Nombre del archivo CSV
archivo_csv = 'datos4.csv'

# Variables para almacenar los datos
b = None
a = []

# Abrir el archivo CSV y leer los datos
with open(archivo_csv, 'r') as f:
    # Leer la primera línea y convertirla en lista de enteros
    b = [int(num) for num in f.readline().strip().split(',')]

    # Leer las líneas restantes y convertirlas en listas de enteros
    for linea in f:
        numeros = [int(num) for num in linea.strip().split(',')]
        a.append(numeros)


print("Vector B:", b)
print("Matriz A:", a)

a = np.array(a)
b = np.array(b)

graficar_sistema_ecuaciones(a,b)

