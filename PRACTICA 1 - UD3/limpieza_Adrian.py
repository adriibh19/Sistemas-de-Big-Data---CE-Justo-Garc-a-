import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import re

#REQUISITO: Identidad
print("Iniciando limpieza de Adrián Buenavida.....") 


# PASO 1: Carga y Análisis Inicial del Dataset
    #CARGA DEL DATASET
df = pd.read_csv('ventas_big_data_ut3.csv') 

    #ANÁLISIS INICIAL
print("\n --> Paso 1: Estructura original del dataset")
print(df.info()) 


# PASO 2: Fase de Limpieza Estructural
    #2.1 Eliminación de duplicados 
df_sin_duplicados = df.drop_duplicates() 
filas_duplicadas = len(df) - len(df_sin_duplicados) #esto nos dice cuántas filas se han eliminado


    #2.2 Filtrado de registros que son negativos en la columna 'cantidad'
    #vemos cuántos hay antes de borrarlos 
registros_negativos = len(df_sin_duplicados[df_sin_duplicados['cantidad'] < 0]) 

    #Calculamos la mediana de la columna cantidad (de valores positivos) para sustituir leuego los negativos
mediana_cantidad = df_sin_duplicados.loc[df_sin_duplicados['cantidad'] >= 0, 'cantidad'].median()

    #reemplazamos los valores negativos por la mediana calculada anteriormente
df_sin_duplicados.loc[df_sin_duplicados['cantidad'] < 0, 'cantidad'] = mediana_cantidad

    #Creamos el dataframe para el siguiente paso 
df_paso2 = df_sin_duplicados.copy()

print(f"\n --> Paso 2: Limpieza estructural finalizada")
print(f"Total filas eliminadas por duplicidad: {filas_duplicadas}")
print(f"Total registros negativos corregidos (hecho con la mediana): {registros_negativos}")
print(f"Valor de la mediana aplicada a cantidades: {mediana_cantidad}")



#PASO 3: Fase de transformación (precios y normalización)

    #3.1 Tratamos  precios
df_paso2['precio'] = pd.to_numeric(df_paso2['precio'], errors='coerce') #Con errors=coerce convertimos los "ERR" en valores nulos) para poder operar con ellos luego

    #Calculamos la mediana de los precios para rellenar esos huecos
mediana_precios = df_paso2['precio'].median() 

    #Rellenamos los nulos con la mediana calculada
df_paso2['precio'] = df_paso2['precio'].fillna(mediana_precios) 

    #3.2 Normalización de la columna producto
    #strip() para quitar espacios q ue sobran y capitalize() para que la primera letra sea mayúscula
df_paso2['producto'] = df_paso2['producto'].str.strip().str.capitalize() 

print(f"\n --> Paso 3: Transformación finalizada")
print(f"Mediana calculada para los precios: {mediana_precios:.2f}")


#PASO 4: Fechas
def limpiar_fecha(fecha_str):
    fecha_str = str(fecha_str).lower().strip()

    #Obtenemos la fecha de hoy 
    hoy = datetime.now() 
    
    #4.1"ayer"
    if 'ayer' in fecha_str:
        return (hoy - timedelta(days=1)).strftime('%Y-%m-%d')
    
    #4.2"hace X dias" 
    match = re.search(r'hace (\d+) dias', fecha_str)   #re.search busca un patrón de texto. ejem: 'hace (\d+) dias' -> busca la palabra "hace", luego el número (\d+) y termina en "dias"
    if match:
        dias = int(match.group(1))
        return (hoy - timedelta(days=dias)).strftime('%Y-%m-%d')
    
    #4.3 convertimos formatos estándar (como 12/05/2024) a ISO (2024-05-12)
    try:
        return pd.to_datetime(fecha_str).strftime('%Y-%m-%d')
    
    except:
        return fecha_str


#Aplicamos función a la columna fecha
df_paso2['fecha'] = df_paso2['fecha'].apply(limpiar_fecha)


print(f"\n --> Paso 4: Procesamiento de fechas finalizado")
print("Muestra de fechas transformadas:")
print(df_paso2[['id', 'fecha']].head(10))


#PASO 5:Exportación (bitácora)

#5.1 Exportamos a JSON
nombre_salida = 'ventas_limpias_AdrianBuenavida.json'
df_paso2.to_json(nombre_salida, orient='records', indent=4)  #Guardamos los datos limpios en un archivo .json 

#5.2 Impresión de bitácora  
print("\n")
print("        BITÁCORA - ADRIÁN BUENAVIDA")
print("\n")

print(f"Total de filas iniciales:               {len(df)}")
print(f"Filas eliminadas por duplicidad:        {filas_duplicadas}")
print(f"Registros negativos corregidos:         {registros_negativos}")
print(f"Mediana aplicada a precios:             {mediana_precios:.2f}")
print(f"Archivo de salida generado:             {nombre_salida}")

print("\n")
print("Limpieza de datos finalizada con éxito!!!!!")