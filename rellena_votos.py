import pandas as pd

# Cargar los datos de elecciones y partidos clasificados
elecciones_db_path = "eleccionesDB.csv"
partidos_clasificados_path = "partidos_clasificados.csv"

print("Cargando archivos...")

elecciones_db = pd.read_csv(elecciones_db_path, encoding="utf-8", low_memory=False)
partidos_clasificados = pd.read_csv(partidos_clasificados_path, encoding="utf-8", low_memory=False)

print("Archivos cargados.")

# Cargar el archivo 10xxaamm.DAT
dat_file_path = "02199603_MESA/10029603.DAT"
dat_columns = [
    (0, 2, "Tipo Elección"), (2, 6, "Año"), (6, 8, "Mes"), (8, 9, "Vuelta"),
    (9, 11, "Código Comunidad"), (11, 13, "Código Provincia"), (13, 16, "Código Municipio"),
    (16, 18, "Distrito"), (18, 22, "Código Sección"), (22, 23, "Código Mesa"),
    (23, 29, "Código Candidatura"), (29, 36, "Votos")
]

print("Procesando archivo DAT...")

data = []
with open(dat_file_path, "r", encoding="utf-8") as f:
    for line in f:
        row = {col_name: line[start:end].strip() for start, end, col_name in dat_columns}
        data.append(row)

print("Archivo DAT procesado.")

dat_df = pd.DataFrame(data)

dat_df["Código Candidatura"] = dat_df["Código Candidatura"].astype(int)
dat_df["Votos"] = dat_df["Votos"].astype(int)

print("Procesando clasificación de partidos...")

# Merge con partidos clasificados
merged_df = dat_df.merge(partidos_clasificados, left_on="Código Candidatura", right_on="Código", how="left")

clasificacion_map = {
    "Derecha": "Votos derecha",
    "Izquierda": "Votos izquierda",
    "Centro izquierda": "Votos centro izquierda",
    "Centro derecha": "Votos centro derecha",
    "Regionalista izquierda": "Votos regionalista izquierda",
    "Regionalista derecha": "Votos regionalista derecha"
}


print("Clasificación de partidos procesada.")

# Inicializar columnas en eleccionesDB con 0
elecciones_db[[
    "Votos derecha", "Votos izquierda", "Votos centro izquierda", "Votos centro derecha", 
    "Votos centro derecha", "Votos regionalista izquierda", "Votos regionalista derecha"
]] = 0

print("Asignando votos a eleccionesDB...")

# Asignar votos según clasificación
def asignar_votos(row, elecciones_db):
    filtro = (
        (elecciones_db["Año"] == int(row["Año"])) &
        (elecciones_db["Codigo de MESA"] == row["Código Mesa"]) &
        (elecciones_db["Provincia"] == int(row["Código Provincia"])) &
        (elecciones_db["Municipio"] == int(row["Código Municipio"])) &
        (elecciones_db["Comunidad"] == int(row["Código Comunidad"])) &
        (elecciones_db.index == row.name)  # Asegurar coincidencia exacta por fila
    )
    
    clasificacion = row["Clasificacion"]
    if clasificacion in clasificacion_map:
        elecciones_db.loc[filtro, clasificacion_map[clasificacion]] += row["Votos"]

print("Votos asignados.")
merged_df.apply(lambda row: asignar_votos(row, elecciones_db), axis=1)

print("Votos mergeados 2.")

# Guardar el nuevo archivo
elecciones_db.to_csv("eleccionesDB_actualizado.csv", index=False, encoding="utf-8")
print("Proceso completado. Archivo guardado como eleccionesDB_actualizado.csv")