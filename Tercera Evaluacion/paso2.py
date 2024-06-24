import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit, OptimizeWarning
import warnings
import csv

archivo_csv = 'datos2.csv'

x2_data = []
y2_data = []

with open(archivo_csv, mode='r') as file:
    reader = csv.reader(file)
    next(reader)  # Saltar la primera línea (encabezados)
    for row in reader:
        if len(row) >= 4:  # Asegurarse de que la fila tenga al menos cuatro valores
            x2_data.append(float(row[2]))
            y2_data.append(float(row[3]))

# Convertir listas a vectores de NumPy
x_data = np.array(x2_data)
y_data = np.array(y2_data)


# Grado del polinomio
grado = 4  # Puedes cambiar este valor según necesites

# Definir el polinomio como una suma de términos
def polinomio(x, *coefs):
    return sum(coefs[i] * x**i for i in range(len(coefs)))

# Ajuste del polinomio de grado 'grado' usando scipy.optimize.curve_fit
coefs_iniciales = np.ones(grado + 1)  # Coeficientes iniciales de prueba

with warnings.catch_warnings():
    warnings.simplefilter('ignore', OptimizeWarning)
    #El piso es para ignorar la matriz de covarianza que devuelve curve_fit
    coefs, _ = curve_fit(lambda x, *coefs: polinomio(x, *coefs), x_data, y_data, p0=coefs_iniciales)

# Valores para graficar la curva ajustada
x_vals = np.linspace(0, 4, 100)
y_vals = sum(coefs[i] * x_vals**i for i in range(len(coefs)))

# Gráfico de los datos y la curva ajustada
plt.scatter(x_data, y_data, label='Datos experimentales', color='red')
plt.plot(x_vals, y_vals, label=f'Polinomio de grado {grado}', color='blue')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Ajuste de Polinomio por Mínimos Cuadrados')
plt.legend()
plt.show()

# Mostrar los coeficientes del polinomio ajustado
#print(f"Coeficientes del polinomio ajustado: {coefs}")
