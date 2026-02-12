import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#PASO 1: CARGA Y DESCRIBE 
df = pd.read_csv('misiones_limpias.csv')
print("--->> Perfil del ninja promedio")
print(df['Nivel_Chakra'].describe())




#PASO 2: BOXPLOT 

plt.figure(figsize=(8, 6))
sns.boxplot(y=df['Nivel_Chakra'], color='orange')
plt.title('Detección de OUTLIERS: Nivel de chakra')
plt.ylabel('Cantidad de chakra')

#Esto nos guardará la imagen en la carpeta donde tenemos el script
plt.savefig('boxplot_chakra.png') 
plt.show()






#PASO 3: Z-SCORE 
#Calculamos cuánto se aleja cada ninja de la media
df['Z-Score'] = (df['Nivel_Chakra'] - df['Nivel_Chakra'].mean()) / df['Nivel_Chakra'].std()

#Filtramos a los traidores que superan las 3 desviaciones estándar
traidores = df[df['Z-Score'].abs() > 3]

print("\n--->> Registro del traidor detectado")
print(traidores)






#PASO 4: CAZA MAYOR 

#1. Buscamos ninjas con chakra negativo (que es imposible y podría indicar manipulación de datos o traición)
chakra_negativo = df[df['Nivel_Chakra'] < 0]
print("\n--->> Ninjas con chakra negativo")

print(chakra_negativo)


#2. Buscamos ninjas de la aldea desconocida
aldea_desconocida = df[df['Aldea'] == 'Desconocida']
print("\n--->> Ninjas de aldea desconoccida")

print(aldea_desconocida)


#3. comprobamos su hay o no super ninjas (Z entre 2 y 3)
super_ninjas = df[(df['Z-Score'].abs() > 2) & (df['Z-Score'].abs() <= 3)]
print("\n--->> Super ninjas detectados (Z entre 2 y 3)")

print(super_ninjas)




# Mostramos todos los datos del sospechoso principal que supera las 3 desviaciones estándar
print("\n--- Informe Final del Sospechoso ---")
infiltrado_alto = traidores[traidores['Z-Score'] > 3]
print(infiltrado_alto)