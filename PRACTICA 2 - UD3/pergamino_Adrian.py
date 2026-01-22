import requests
import time
import pandas as pd


#PASO 0:
#Identidad, para saber que soy yo quien ha hecho este pergamino
print("Iniciando extracción por parte de Adrián Buenavida......")


#PASO 1: Navegación por el oergamino infinito (Paginación de la api)
#Configuración inicial de variables 
url_inicial = "https://pokeapi.co/api/v2/pokemon?limit=100"     #de 100 en 100 para ir rápido
url_actual = url_inicial
lista_pokemon_basica = []

print("\n --> PASO 1: Iniciando navegación por el pergamino infinito")

#Bucle para recorrer la paginación de la API de Pokemon
while url_actual:
    print(f"Consultando página: {url_actual}")
    
    respuesta = requests.get(url_actual)
    datos = respuesta.json()
    
    #Añadimos los resultados actuales (nombre y url de detalle) a nuestra lista
    lista_pokemon_basica.extend(datos['results'])
    
    #Actualizamos la URL con el enlace a la siguiente página
    url_actual = datos['next']
    
    #Pequeña pausa para no saturar l API
    time.sleep(0.2)

print(f"\n 1a extracción acabada!!! . Hemos detectado {len(lista_pokemon_basica)} Pokeemon")




#PASO 2 (mejor opcion y más rápida): detalles individuales de cada Pokémon

print("\n--> PASO 2: Extrayendo detalles individuales de cada Pokémon...")

datos_finales = []

#Limitamos a los primeros 30 para que el script termine rápido 
for pokemon in lista_pokemon_basica[:30]:
    res_detalle = requests.get(pokemon['url'])
    d = res_detalle.json()
    
    #Extraemos solo los 4 campos que nos pide la práctica
    datos_finales.append({
        'name': d['name'],
        'height': d['height'],
        'weight': d['weight'],
        'base_experience': d['base_experience']
    })
    print(f"Ninja extraído: {d['name']}")

#Creamos el DataFrame
df = pd.DataFrame(datos_finales)

print("\n --> Paso 2 finalizado con éxito !!!")
print(df.head())



#opción que tenía puesta al principio, pero muchísima mas lenta porque hacía muchas peticiones

#print("\n--> PASO 2: Iniciando LA EXTRACCIÓN de detalles individuales")

#datos_finales = []
#contador = 0

#Recorremos lista de URLs que conseguimos en el paso1
#for pokemon in lista_pokemon_basica:
#    contador += 1

 #   #hacemos la petición al detalle de cada pokemon
  #  res_detalle = requests.get(pokemon['url'])
   # d = res_detalle.json()
    
    #Extraemos solo los 4 campos que nos pide l
    #info_pokemon = {
     #   'name': d['name'],
      #  'height': d['height'],
       # 'weight': d['weight'],
        #'base_experience': d['base_experience']
    #}
    
    #datos_finales.append(info_pokemon)
    
    #Imprimimos 2000 para no saturar
    #if contador % 200 == 0:
     #   print(f"Procesados {contador} de {len(lista_pokemon_basica)} ninjas...")

#Convertimos nuestra lista en un df de pandas
#df = pd.DataFrame(datos_finales)

#print("\n extracción finalizada con éxito !!!")
#print(df.head())





#PASO 3: IMC
print("\n--> PASO 3: Calculando el IMC...")

#Convertimos las unidades de la API a metros y kilos
df['height_m'] = df['height'] / 10
df['weight_kg'] = df['weight'] / 10
df['bmi'] = (df['weight_kg'] / (df['height_m'] ** 2)).round(2)

print(df[['name', 'height_m', 'weight_kg', 'bmi']].head())



# PASO 4: Guardado
print("\n--> PASO 4: Guardando pergamino...")
df.to_csv("pergamino_AdrianBuenavida.csv", index=False)

print("Archivo generado con éxito!")







