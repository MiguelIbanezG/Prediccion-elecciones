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

# Diccionarios de mapeo de códigos
comunidades = {
    "01": "Andalucía", "02": "Aragón", "03": "Asturias", "04": "Baleares",
    "05": "Canarias", "06": "Cantabria", "07": "Castilla - La Mancha", "08": "Castilla y León",
    "09": "Cataluña", "10": "Extremadura", "11": "Galicia", "12": "Madrid",
    "13": "Navarra", "14": "País Vasco", "15": "Región de Murcia", "16": "La Rioja",
    "17": "Comunidad Valenciana", "18": "Ceuta", "19": "Melilla"
}

codigo_a_provincia = {
    "01": "Álava", "02": "Albacete", "03": "Alicante", "04": "Almería", "05": "Ávila",
    "06": "Badajoz", "07": "Islas Baleares", "08": "Barcelona", "09": "Burgos", "10": "Cáceres",
    "11": "Cádiz", "12": "Castellón", "13": "Ciudad Real", "14": "Córdoba", "15": "A Coruña",
    "16": "Cuenca", "17": "Girona", "18": "Granada", "19": "Guadalajara", "20": "Gipuzkoa",
    "21": "Huelva", "22": "Huesca", "23": "Jaén", "24": "León", "25": "Lleida",
    "26": "La Rioja", "27": "Lugo", "28": "Madrid", "29": "Málaga", "30": "Murcia",
    "31": "Navarra", "32": "Ourense", "33": "Asturias", "34": "Palencia", "35": "Las Palmas",
    "36": "Pontevedra", "37": "Salamanca", "38": "Santa Cruz de Tenerife", "39": "Cantabria",
    "40": "Segovia", "41": "Sevilla", "42": "Soria", "43": "Tarragona", "44": "Teruel",
    "45": "Toledo", "46": "Valencia", "47": "Valladolid", "48": "Bizkaia", "49": "Zamora",
    "50": "Zaragoza", "51": "Ceuta", "52": "Melilla"
}

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

# Reemplazar códigos por nombres
df["Comunidad"] = df["Comunidad"].map(comunidades).fillna(df["Comunidad"])
df["Provincia"] = df["Provincia"].map(codigo_a_provincia).fillna(df["Provincia"])

# Guardar de nuevo el archivo CSV
df.to_csv(nombre_fichero_csv, index=False, encoding="utf-8")

print(f"Fichero CSV '{nombre_fichero_csv}' actualizado correctamente con los datos y nombres reemplazados.")
