import pandas as pd

# Parámetros del archivo de entrada y salida
nombre_fichero_csv = "edad_media.csv"
nombre_fichero_salida = "ganadora.csv"

# Definir las candidaturas ganadoras por año (debes modificar esta lista según los datos reales)
candidaturas_ganadoras = {
    "1996": "PSOE",
    "2000": "PP",
    "2004": "PP",
    "2008": "PSOE",
    "2011": "PSOE",
    "2015": "PP",
    "2019": "PP",
    "2023": "PSOE"
}

# Cargar el archivo CSV
df = pd.read_csv(nombre_fichero_csv, dtype=str)

# Rellenar la columna de candidatura ganadora según el año
df["Candidatura Ganadora"] = df["Año"].map(candidaturas_ganadoras)

# Guardar el archivo actualizado
df.to_csv(nombre_fichero_salida, index=False, encoding="utf-8")

print(f"Fichero CSV '{nombre_fichero_salida}' generado correctamente con la candidatura ganadora por año.")