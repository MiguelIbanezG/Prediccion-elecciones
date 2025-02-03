import csv
import pandas as pd

# Parámetros del archivo de entrada y salida
nombre_fichero_dat = "02199603_MESA/09029603.DAT"  # Ajustar según la elección específica
nombre_fichero_csv = "eleccionesDB.csv"

# Definición de posiciones según la documentación
posiciones = {
    "codigo_mesa": (23, 23),
    "codigo_comunidad": (10, 11),
    "codigo_provincia": (12, 13),
    "codigo_municipio": (14, 16),
}

def extraer_valor(linea, inicio, fin):
    """Extrae un valor de una línea dado un rango de posiciones."""
    return linea[inicio-1:fin].strip()

# Cargar el archivo CSV existente
df = pd.read_csv(nombre_fichero_csv, dtype=str)

# Procesar el fichero .DAT
nuevas_filas = []
with open(nombre_fichero_dat, "r", encoding="latin-1") as infile:
    for linea in infile:
        codigo_mesa = extraer_valor(linea, *posiciones["codigo_mesa"])
        codigo_comunidad = extraer_valor(linea, *posiciones["codigo_comunidad"])
        codigo_provincia = extraer_valor(linea, *posiciones["codigo_provincia"])
        codigo_municipio = extraer_valor(linea, *posiciones["codigo_municipio"])
        
        nuevas_filas.append(["1996", codigo_mesa, codigo_comunidad, codigo_provincia, codigo_municipio])

# Convertir las nuevas filas en un DataFrame
df_nuevo = pd.DataFrame(nuevas_filas, columns=df.columns[:5])

# Agregar los nuevos datos al DataFrame existente
df = pd.concat([df, df_nuevo], ignore_index=True)

# Guardar de nuevo el archivo CSV
df.to_csv(nombre_fichero_csv, index=False, encoding="utf-8")

print(f"Fichero CSV '{nombre_fichero_csv}' actualizado correctamente.")

