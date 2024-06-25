import numpy as np
from sympy import symbols, lambdify, expand
import matplotlib.pyplot as plt
import csv


def trazador_cubico(xi, yi):
    n = len(xi)
    
    # Calculando los valores de h
    h = np.zeros(n-1)
    for j in range(n-1):
        h[j] = xi[j+1] - xi[j]
    
    # Sistema de ecuaciones
    A = np.zeros((n-2, n-2))
    B = np.zeros(n-2)
    S = np.zeros(n)
    
    A[0, 0] = 2 * (h[0] + h[1])
    A[0, 1] = h[1]
    B[0] = 6 * ((yi[2] - yi[1]) / h[1] - (yi[1] - yi[0]) / h[0])
    
    for i in range(1, n-3):
        A[i, i-1] = h[i]
        A[i, i] = 2 * (h[i] + h[i+1])
        A[i, i+1] = h[i+1]
        factor21 = (yi[i+2] - yi[i+1]) / h[i+1]
        factor10 = (yi[i+1] - yi[i]) / h[i]
        B[i] = 6 * (factor21 - factor10)
    
    A[n-3, n-4] = h[n-3]
    A[n-3, n-3] = 2 * (h[n-3] + h[n-2])
    factor12 = (yi[n-1] - yi[n-2]) / h[n-2]
    factor23 = (yi[n-2] - yi[n-3]) / h[n-3]
    B[n-3] = 6 * (factor12 - factor23)
    
    # Resolviendo el sistema de ecuaciones para S
    r = np.linalg.solve(A, B)
    for j in range(1, n-1):
        S[j] = r[j-1]
    S[0] = 0
    S[n-1] = 0
    
    # Calculando los coeficientes a, b, c, d
    a = np.zeros(n-1)
    b = np.zeros(n-1)
    c = np.zeros(n-1)
    d = np.zeros(n-1)
    for j in range(n-1):
        a[j] = (S[j+1] - S[j]) / (6 * h[j])
        b[j] = S[j] / 2
        factor10 = (yi[j+1] - yi[j]) / h[j]
        c[j] = factor10 - (2 * h[j] * S[j] + h[j] * S[j+1]) / 6
        d[j] = yi[j]
    
    # Construyendo los polinomios por tramos
    x = symbols("x")
    px_tabla = []
    for j in range(n-1):
        pxtramo = a[j] * (x - xi[j])**3 + b[j] * (x - xi[j])**2
        pxtramo += c[j] * (x - xi[j]) + d[j]
        pxtramo = expand(pxtramo)
        px_tabla.append(pxtramo)
    
    return px_tabla

# Nombre del archivo CSV
archivo_csv = 'datos1.csv'

# Listas para almacenar los valores de x e y
xi_1 = []
yi_1 = []

# Lectura del archivo CSV
with open(archivo_csv, newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        # Convertir cada elemento de la fila de string a float
        valores = [float(valor) for valor in row]
        # Almacenar en x (primera fila) y y (segunda fila)
        if len(xi_1) == 0:
            xi_1= valores
        else:
            yi_1 = valores

# Imprimir las listas x e y
print("Valores de x:", xi_1)
print("Valores de y:", yi_1)


muestras = 100

px_tabla = trazador_cubico(xi_1, yi_1)

print("Polinomios por tramos:")
for tramo in range(len(xi_1)-1):
    print(f"x = [{xi_1[tramo]}, {xi_1[tramo+1]}]")
    print(f"{px_tabla[tramo]}\n")

x = symbols("x")
xtraza = []
ytraza = []
for tramo in range(len(xi_1)-1):
    a = xi_1[tramo]
    b = xi_1[tramo+1]
    xtramo = np.linspace(a, b, muestras)
    
    # Evaluando el polinomio del tramo
    pxtramo = px_tabla[tramo]
    pxt = lambdify(x, pxtramo, modules='numpy')
    ytramo = pxt(xtramo)

    # Concatenando los vectores de trazador en x,y
    xtraza.extend(xtramo)
    ytraza.extend(ytramo)

# Graficando
plt.scatter(xi_1, yi_1, label="puntos", color='red')
plt.plot(xtraza, ytraza, label="trazador", color='blue')
plt.title("Trazador Cúbico")
plt.xlabel("xi")
plt.ylabel("px(xi)")
plt.legend()
plt.show()
