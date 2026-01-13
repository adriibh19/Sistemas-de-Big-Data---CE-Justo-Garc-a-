import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import re

# --- REQUISITO: Identidad ---
print("Iniciando limpieza de Adrián Buenavida...") #

# PASO 1: Carga del dataset y análisis inicial
# Cargamos el archivo CSV y mostramos info inicial para la documentación
df = pd.read_csv('ventas_big_data_ut3.csv') #
total_inicial = len(df)
print("\n--- Paso 1: Análisis inicial del Dataset ---")
print(df.info()) #

# PASO 2: Fase de Limpieza Estructural
# Eliminamos duplicados exactos (donde toda la fila coincide)
df_sin_duplicados = df.drop_duplicates() #
filas_duplicadas = total_inicial - len(df_sin_duplicados)

# Filtramos cantidades negativas (errores de entrada)
registros_negativos = len(df_sin_duplicados[df_sin_duplicados['cantidad'] < 0]) #
df_paso2 = df_sin_duplicados[df_sin_duplicados['cantidad'] >= 0].copy() #

# PASO 3: Fase de Transformación (Precios y Normalización)
# Convertimos 'precio' a numérico: los "ERR" se convierten en NaN automáticamente
df_paso2['precio'] = pd.to_numeric(df_paso2['precio'], errors='coerce') #

# Imputamos la mediana para los valores faltantes o erróneos
mediana_precios = df_paso2['precio'].median() #
df_paso2['precio'] = df_paso2['precio'].fillna(mediana_precios) #

# Normalizamos el nombre del producto (Capitalizado y sin espacios extra)
df_paso2['producto'] = df_paso2['producto'].str.strip().str.capitalize() #

# PASO 4: Procesamiento de Fechas (ISO y Relativas)
def limpiar_fecha(fecha_str):
    fecha_str = str(fecha_str).lower().strip()
    hoy = datetime.now() #
    
    # Manejo de fechas relativas
    if 'ayer' in fecha_str:
        return (hoy - timedelta(days=1)).strftime('%Y-%m-%d') #
    
    match = re.search(r'hace (\d+) dias', fecha_str) #
    if match:
        dias = int(match.group(1))
        return (hoy - timedelta(days=dias)).strftime('%Y-%m-%d')
    
    # Estandarización a formato ISO (YYYY-MM-DD)
    try:
        return pd.to_datetime(fecha_str, dayfirst=False).strftime('%Y-%m-%d')
    except:
        return fecha_str

df_paso2['fecha'] = df_paso2['fecha'].apply(limpiar_fecha) #

# PASO 5: Exportación y Reporte Final
archivo_salida = "ventas_limpias_AdrianBuenavida.json" #
df_paso2.to_json(archivo_salida, orient='records', indent=4) #

# --- REQUISITO: Bitácora de Limpieza ---
print("\n" + "="*50)
print("       BITÁCORA DE LIMPIEZA - ADRIÁN BUENAVIDA")
print("="*50)
print(f"Total de filas iniciales:                {total_inicial}") #
print(f"Filas eliminadas por duplicidad:         {filas_duplicadas}") #
print(f"Valor de la mediana (Precios):           {mediana_precios:.2f}") #
print(f"Registros negativos descartados:         {registros_negativos}") #
print(f"Archivo de salida generado:              {archivo_salida}") #
print("="*50)