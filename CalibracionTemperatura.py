import os
import pandas as pd

# Path
carpeta = r"C:\Users\ernes\Documents\Laboratorio\LaboratorioTeledeteccion\Datos In situ"

# Obtén la lista de archivos en la carpeta
archivos_excel = [archivo for archivo in os.listdir(carpeta) if archivo.endswith(".xls")]

# Crea una lista para almacenar los dataframes de cada archivo
dataframes = []

# Lee cada archivo Excel y agrega su contenido al dataframe
for archivo in archivos_excel:
    ruta_archivo = os.path.join(carpeta, archivo)
    df = pd.read_excel(ruta_archivo)
    dataframes.append(df)

# Combina todos los dataframes en uno solo
dataframe_final = pd.concat(dataframes)