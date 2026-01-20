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

print(f"\n Extracción acabada!!! . Hemos detectado {len(lista_pokemon_basica)} Pokeemon")




#PASO 2: Extracción de detalles individuales de cada Pokémon
print("\n--> PASO 2: Iniciando LA EXTRACCIÓN de detalles individuales")

datos_finales = []
contador = 0

#Recorremos lista de URLs que conseguimos en el paso1
for pokemon in lista_pokemon_basica:
    contador += 1

    #hacemos la petición al detalle de cada pokemon
    res_detalle = requests.get(pokemon['url'])
    d = res_detalle.json()
    
    #Extraemos solo los 4 campos que nos pide l
    info_pokemon = {
        'name': d['name'],
        'height': d['height'],
        'weight': d['weight'],
        'base_experience': d['base_experience']
    }
    
    datos_finales.append(info_pokemon)
    
    #Imprimimos 100 para no saturar
    if contador % 100 == 0:
        print(f"Procesados {contador} de {len(lista_pokemon_basica)} ninjas...")

#Convertimos nuestra lista en un df de pandas
df = pd.DataFrame(datos_finales)

print("\n extracción finalizada con éxito !!!")
print(df.head())

