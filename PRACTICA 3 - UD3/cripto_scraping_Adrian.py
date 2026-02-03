import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

#PASO 0: Identidad
print("Iniciando el scraping de CoinMarketCap - Adrián Buenavida...")

#PASO 1: Configuramos de cabeceras (Disfraz), para que no nos rechacen peticiones 
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
}

lista_criptos = []

#PASO 3: Gestión de la paginación (500 monedas)
#como CoinMarketCap muestra 100 resultados por página. Del 1 al 5 tenemos las 500
print("\n --> PASO 1 y 3: Navegando por las 5 páginas para obtener 500 registros.....")


for pagina in range(1, 6):              #para que coga las páginas del 1 al 5    
    url = f"https://coinmarketcap.com/?page={pagina}"
    print(f"Procesando página {pagina}: {url}")
    
    response = requests.get(url, headers=headers, timeout=15)
    if response.status_code != 200:
        print(f"Error al acceder a la página {pagina}")
        continue
        
    soup = BeautifulSoup(response.text, 'html.parser')
    
    #Localizamos todas las filas de la tabla
    filas = soup.find_all('tr')

    for fila in filas:
        celdas = fila.find_all('td')
        

        if len(celdas) > 9: 
            #PASO 2: Extraemos de campos obligatorios
            try:
                texto_identidad = celdas[2].find_all('p', class_='coin-item-name')[0].text
                simbolo = celdas[2].find_all('p', class_='coin-item-symbol')[0].text

                #añadimos los datos a la lista
                lista_criptos.append({
                    'Nombre': texto_identidad,
                    'Símbolo': simbolo,
                    'Precio': celdas[3].find_all('span')[0].text,
                    'Market Cap': celdas[7].find_all('span')[0].text,
                    'Volumen 24h': celdas[8].find_all('p')[0].text,
                })
            except:
                continue

        #si no encuentra el nombre, lo busca en la etiqueta span
        else:

            try:
                #try para evitar el IndexError
                spans = fila.find_all('span')

                if len(spans) > 2:              #comprobamos que tiene mínimo de spans
                    texto_identidad = spans[1].text
                    
                    #añadimos solo si la fila tiene celdas suficientes para el precio
                    if len(celdas) > 3:

                        print(celdas[3])
                        lista_criptos.append({
                            'Nombre': texto_identidad,
                            'Símbolo': "N/A",
                            'Precio': celdas[3].text,
                            
                            
                        })

                        
            except Exception as e:
                print(f"Error procesando fila: {e}")
                continue

    #pausaparaevitarbloqueos
    time.sleep(2)

    #PASO 4: Guardado en CSV
df_final = pd.DataFrame(lista_criptos)
df_final.to_csv("cripto_data.csv", index=False)

#MENSAJE FINAL DE ÉXITO
print(f"\n¡Misión cumplida! Se han guardado {len(df_final)} monedas en 'cripto_data.csv'.")
print("Muestra de los primeros datos:")
print(df_final.head())