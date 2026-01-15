import pandas as pd
import numpy as np

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