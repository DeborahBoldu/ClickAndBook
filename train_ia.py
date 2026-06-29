import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib
import os

def generar_modelo_precios():
    np.random.seed(13)
    n = 1000

    duracion = np.random.randint(1, 7, n)
    valoracion = np.random.uniform(1.0, 5.0, n)
    precio = 1500 + (duracion * 2500) + (valoracion * 1200) + np.random.normal(0, 500, n)

    df = pd.DataFrame({'duracion': duracion, 'valoracion': valoracion, 'precio': precio})
    X = df[['duracion', 'valoracion']]
    y = df['precio']

    modelo = LinearRegression()
    modelo.fit(X, y)

    os.makedirs('app/services', exist_ok=True)
    joblib.dump(modelo, 'app/services/modelo_precio_ia.joblib')
    print("modelo guardado.")

if __name__ == "__main__":
    generar_modelo_precios()
