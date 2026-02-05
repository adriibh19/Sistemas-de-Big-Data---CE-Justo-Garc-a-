import pandas as pd

#1. Carga del pergamino secreto 
print("Iniciando rastreo de chakra de Adrián Buenavida...")
df = pd.read_csv('registros_misiones.csv')

#1 --> LIMPIEZA DE DATOS

def limpiar_registro(df):
    #Reto 1: Elimina filas duplicadas
    df = df.drop_duplicates()
    
    #Reto 2: Estandarizamos la columna 'aldea' 
    df['aldea'] = df['aldea'].str.strip().str.replace('_', '').str.capitalize() #elimina espacios, guiones bajos y PONE MAYÚSC
    df['aldea'] = df['aldea'].replace('Lluvia', 'Amegakure')  #corregimos el nombre de la aldea de la lluvia
    
    #Reto 3: Identidad en la Niebla 
    df.loc[(df['nin_id'].isna()) & (df['aldea'] == 'Kiri'), 'nin_id'] = 'Ninja de la niebla anonimooo'   #asignamos un nombre genérico a los ninjas sin ID de la aldea de la niebla
    
    #Reto 4: Convertimos ts a datetime 
    df['ts'] = pd.to_datetime(df['ts'])     #convertimos la columna de timestamp a formato datetime para facilitar el análisis temporal
    
    #Reto 5: Filtramos niveles de chakra imposibles  
    df = df[(df['chakra'] > 0) & (df['chakra'] <= 100000)]
    
    #Reto 6: Renombramos las columnas para mayor claridad
    df = df.rename(columns={
        'id_reg': 'ID', 'ts': 'Fecha', 'nin_id': 'Ninja', 'status': 'Estado', 'desc': 'Descripcion'
    })

    return df

#Ejecutamos la función de limpieza
df_limpio = limpiar_registro(df)



#2 --> BÚSQUEDA Y CONSULTAS 

def realizar_consultas(df):
    print("\n  INICIANDO BÚSQUEDA ANBU ")

    #Reto 7: Palabras clave de amenazas 
    amenazas = df[df['Descripcion'].str.contains('espía|sospechoso|enemigo', case=False)]  #filtramos las misiones que contienen palabras clave relacionadas con amenazas grandes, sin importar mayúsculas o minúsculas
    print(f"\n --> Amenazas detectadas (Reto 7): {len(amenazas)} registros")
    print(amenazas.head(3))


    #Reto 8: Infiltrados de la lluvia 
    infiltrados_lluvia = df[(df['aldea'] == 'Amegakure') & (df['chakra'] > 5000) & (df['rango'] != 'D')] #filtramos los registros de la aldea de la lluvia con niveles de chakra ""sospechosamente" altos y rango que no sea D, lo que podría ser ninjas infiltrados con habilidades avanzadas
    print(f"\n --> Infiltrados de amegakure (Reto 8): {len(infiltrados_lluvia)} ninjas")
    print(infiltrados_lluvia.head(3))


    #Reto 9: Vigilancia nocturna (23:00 a 05:00) 
        #usamos dt.hour para filtrar por hora 
    madrugada = df[(df['Fecha'].dt.hour >= 23) | (df['Fecha'].dt.hour < 5)] #filtramos ocuridos  durante la madrugada, lo que podría indicar actividades sospechosas o misiones nocturnas de alto riesgo

    print(f"\n --> Accesos de madrugada (Reto 9): {len(madrugada)} registros")
    print(madrugada.head(3))


    #Reto 10: Top 5 chakra por aldea 
    top_5_chakra = df.sort_values(['aldea', 'chakra'], ascending=[True, False]).groupby('aldea').head(5)  #ordenamos por aldea y chakra de forma descendente, luego agrupamos por aldea y seleccionamos los 5 registros con mayor chakra parra cada una

    print("\n --> Élite de las aldeas (Reto 10):")
    print(top_5_chakra.head(10))                #mostramos los 10 primeros registros del top 5 de cada aldea para saber más o mnenos los ninjas más poderosos de cada una


    #Reto 11: Ninjas fuera de la Alianza 
    alianza = ['Konoha', 'Suna', 'Kumo']
    extranjeros = df[~df['aldea'].isin(alianza)] #~df es para negar la condición, es decir, seleccionamos los registros cuya aldea no está en la lista de la alianza. el isin devuelve un booleano indicando si cada valor de la columna 'aldea' está en la lista de la alianza

    print(f"\n --> Ninjas fuera de la Alianza (Reto 11): {len(extranjeros)} registros")


    #Reto 12: Misiones fallidas por aldea 
    fallos_por_aldea = df[df['Estado'] == 'Fallo'].groupby('aldea').size()  #filtramos los registros con fallo, luego agrupamos por aldea y contamos el número de fallos para cada una
    print("\n --> Mapa de fallos por aldea (Reto 12):")
    print(fallos_por_aldea)

#EJECUCIÓN FINAL 
realizar_consultas(df_limpio)


#Guardamos el resultado final 
archivo_salida = 'misiones_limpias_Adrian.csv'
df_limpio.to_csv(archivo_salida, index=False)
print(f"\n[+] Pergamino restaurado en: {archivo_salida}")