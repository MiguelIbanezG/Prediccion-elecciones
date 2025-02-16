import pandas as pd

# Cargar el CSV
file_path = 'edad_media.csv'  # Cambia esto por la ruta real
df = pd.read_csv(file_path)

# Seleccionar las columnas de votos
votos_columnas = ['Votos Derecha', 'Votos Izquierda', 'Votos Centro Izquierda', 'Votos Centro Derecha', 'Votos Regionalista Izquierda', 'Votos Regionalista Derecha']

# Convertir a numérico, ignorando errores y reemplazando NaN por 0
df[votos_columnas] = df[votos_columnas].apply(pd.to_numeric, errors='coerce').fillna(0)

# Sumar todos los votos
total_votos = df[votos_columnas].sum().sum()

print(f'Total de votos: {total_votos}')
