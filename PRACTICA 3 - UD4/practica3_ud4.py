import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns


#1. dataset
df = pd.read_csv('aptitudes_ninja.csv')

#2. Selección de características y limpieza
    #Filtramos nulos y valores negativos si los hubiera
df = df.dropna()  #quitamos valores nulos
df = df[(df['fuerza_fisica'] >= 0) & (df['control_chakra'] >= 0)]  #quitamos valores negativos

X = df[['fuerza_fisica', 'control_chakra']]



#3. Escalado de datos con el standard para que caracter tengan la misma importancia 
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)


#PASO 2: ENCONTRAR EL “K” "perfecto/optimo"" (MÉT. DEL CODO) 

#1. Creamos una lista para guardar la inercia de cada K 
inercia = []

#2. Probamos con valores de K del 1 al 10 
for k in range(1, 11):
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(X_scaled)
    inercia.append(kmeans.inertia_)

#3. Dibujamos el gráfico para localizar el "codo", donde la linea deja de bajar fuertemente
plt.figure(figsize=(8, 5))
plt.plot(range(1, 11), inercia, marker='o', linestyle='--', color='blue')
plt.title('Método del codo')
plt.xlabel('Número de unidades (K )')
plt.ylabel('Inercia')

#Guardamos  gráfico 
plt.savefig('metodo_codo.png')
plt.show()

#Tras ver el gráfico, seleccionamos K=4 porque es donde la linea deja de bajar tan bruscamente
k_optimo = 4




#PASO 3: ENTRENAMIENTO Y CLASIFICACIÓN 

#1. Definimos y entrenamos el modelo con K=4 
kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)

    #ponemos a cada ninja su unidad segun lo entrenado, resultado es un nº del 0 al 3 (las 3 uds que hay para clasificar a los ninjjas)
df['unidad_id'] = kmeans.fit_predict(X_scaled)



#2. Obtenemos las coordenadas de los centroides  
centroides = kmeans.cluster_centers_



#PASO 4: SCATTER PLOT

plt.figure(figsize=(10, 7))

#Dibujamos los puntos de los ninjas coloreados por su grupo
sns.scatterplot(x=df['fuerza_fisica'], y=df['control_chakra'], 
                hue=df['unidad_id'], palette='viridis', s=60, alpha=0.7)


#Invertimos el escalado de los centroides para dibujarlos en la escala original (0-100)
centroides_originales = scaler.inverse_transform(centroides)


#Dibujamos los centroides con una "X" roja grande
plt.scatter(centroides_originales[:, 0], centroides_originales[:, 1], 
            c='red', marker='X', s=200, label='Centroides')

plt.title('Mapa de unidades de la alianza shinobi')
plt.xlabel('Fuerza física')
plt.ylabel('Control de chakra')
plt.legend(title='Unidades')
plt.savefig('mapa_unidades.png')
plt.show()




#PASO 5: ANÁLISIS DE PERFILES 

#Calculamos la media de fuerza y chakra para cada grupo para saber quiénes son
perfiles = df.groupby('unidad_id')[['fuerza_fisica', 'control_chakra']].mean()  #agrupamos por unidad_id y calculamos la media de las características para cada grupo

print("\n --> Perfiles promedio por unidad")
print(perfiles)



#esto es para mostrar cómo se han clasificado los ninjas en las unidades, mostrando solo algunas columnas
print("\n --> Muestra de clasificación de ninjas en las unidades que hay: ")
print(df[['nombre_sujeto', 'fuerza_fisica', 'control_chakra', 'unidad_id']].head())



