import pandas as pd
import os

# 📌 Diccionario con las carpetas por año
archivos_dat = {
    "1996": "../Datos_Mesas/02199603_MESA/",
    "2000": "../Datos_Mesas/02200003_MESA/",
    "2004": "../Datos_Mesas/02200403_MESA/",
    "2008": "../Datos_Mesas/02200803_MESA/",
    "2011": "../Datos_Mesas/02201111_MESA/",
    "2015": "../Datos_Mesas/02201512_MESA/",
    "2016": "../Datos_Mesas/02201606_MESA/",
    "2019a": "../Datos_Mesas/02201904_MESA/",
    "2019b": "../Datos_Mesas/02201911_MESA/",
    "2023": "../Datos_Mesas/02202307_MESA/",
}

# 📌 Columnas de los archivos .DAT
dat_columns = {
    "codigo_provincia": (12, 13),
    "censo_ine": (78, 85),
    "total_votantes": (110, 117),
}

# 📌 Diccionario para almacenar la tasa de participación por provincia y año
tasa_participacion_provincia = {}

# 📂 Procesar archivos de cada año
for año, ruta_ficheros in archivos_dat.items():
    if not os.path.exists(ruta_ficheros):
        print(f"⚠️ La ruta {ruta_ficheros} no existe. Omitiendo...")
        continue
    
    # 📂 Buscar archivos 05xxaamm.DAT y 07xxaamm.DAT
    for fichero in os.listdir(ruta_ficheros):
        if fichero.startswith(("05", "07")) and fichero.endswith(".DAT"):
            with open(os.path.join(ruta_ficheros, fichero), "r", encoding="latin-1") as file:
                for linea in file:
                    provincia = linea[dat_columns["codigo_provincia"][0] - 1:dat_columns["codigo_provincia"][1]].strip()
                    censo_str = linea[dat_columns["censo_ine"][0] - 1:dat_columns["censo_ine"][1]].strip()
                    votantes_str = linea[dat_columns["total_votantes"][0] - 1:dat_columns["total_votantes"][1]].strip()

                    # Validar que los valores sean numéricos antes de convertirlos a int
                    if not censo_str.isdigit() or not votantes_str.isdigit():
                        continue

                    censo = int(censo_str)
                    votantes = int(votantes_str)

                    if provincia and censo > 0:
                        tasa_participacion = (votantes / censo) * 100
                        tasa_participacion_provincia[(año, provincia.zfill(2))] = round(tasa_participacion, 2)


# 📂 Cargar el CSV base
df = pd.read_csv("05_votos_sin_duplicados.csv", dtype=str)

# 🔹 Asegurar que la columna Provincia sea de dos dígitos
df["Provincia"] = df["Provincia"].astype(str).str.zfill(2)

# 🔹 Crear la columna "Tasa de Participacion" si no existe
if "Tasa de Participacion" not in df.columns:
    df["Tasa de Participacion"] = ""

# 🔹 Mapear la tasa de participación al CSV basado en Año y Provincia
df["Tasa de Participacion"] = df.apply(
    lambda row: tasa_participacion_provincia.get((row["Ano"], row["Provincia"]), ""), axis=1
)

# 📂 Guardar el CSV modificado
df.to_csv("participacion.csv", index=False, encoding="utf-8")

print("✅ CSV modificado guardado como 'participacion.csv'")
