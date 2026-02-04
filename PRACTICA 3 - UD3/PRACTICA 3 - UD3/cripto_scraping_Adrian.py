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
print("\n --> PASO 1 y 3: Navegando por las 5 páginas para obtener 500 monedas.....")


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

                #PASO 5: Limpieza de datos quitando símbolos y comas
                #limpiamospreciomarketcapyvolumen #taltaltal
                precio_clean = celdas[3].find_all('span')[0].text.replace('$', '').replace(',', '').strip()
                market_clean = celdas[7].find_all('span')[0].text.replace('$', '').replace(',', '').strip()
                volumen_clean = celdas[8].find_all('p')[0].text.replace('$', '').replace(',', '').strip()

                #añadimos los datos a la lista
                lista_criptos.append({
                    'Nombre': texto_identidad,
                    'Símbolo': simbolo,
                    'Precio': precio_clean,
                    'Market Cap': market_clean,
                    'Volumen 24h': volumen_clean,
                })
            except:
                continue

        #si no encuentra el nombre, lo busca en la etiqueta span
        else:
            
            try:
                spans = fila.find_all('span')
                
                if len(spans) > 2:
                    
                    texto_identidad = spans[1].text
                    
                    #Filtro para evitar filas de encabezado o vacías que generan NaN #taltaltal
                    if texto_identidad and texto_identidad.strip() and texto_identidad != "N/A":

                        #PARA EL PRECIO:
                            #En lugar de un IF que descarte la fila, usamos variables vacías
                            #Así, si celdas[7] no existe, el script no explota como me hacía antes y guarda el resto
                        #añadimos limpieza al precio #taltaltal
                        precio = celdas[3].text.replace('$', '').replace(',', '').strip() if len(celdas) > 3 else "0"
                        
                        
                        #PARA EL MARKET CAP:
                            #celda 7 cogmos el 2o span DENTRO DE UN P que es donde se encuentra
                        try:
                            p_cap = celdas[7].find('p')
                            m_cap_raw = p_cap.find_all('span')[1].text if p_cap else celdas[7].text
                            #limpiamos el market cap #taltaltal
                            m_cap = m_cap_raw.replace('$', '').replace(',', '').strip()
                            
                        except:
                            m_cap = "0"
                            
                        
                        #PARA EL VOLUMEN24H:    
                            #Celda 8 está en el primer <p> 
                        try:
                            #Buscamos el primer párrafo que contiene el valor grande en blanco
                            vol_raw = celdas[8].find('p').text if celdas[8].find('p') else celdas[8].text
                            #limpiamos el volumen #taltaltal
                            vol_24h = vol_raw.replace('$', '').replace(',', '').strip()
                            
                        except:
                            vol_24h = "0"


                        lista_criptos.append({
                            'Nombre': texto_identidad,
                            'Símbolo': "N/A",
                            'Precio': precio,
                            'Market Cap': m_cap,
                            'Volumen 24h': vol_24h
                        })
            except:
                continue

    
    time.sleep(2)

#PASO 4: Guardado en CSV
df_final = pd.DataFrame(lista_criptos)


#Eliminamos filas con Nombre "N/A"
df_final = df_final[df_final['Nombre'] != "N/A"]

        #Usamos la ruta absoluta 
import os
ruta_destino = r"C:\Users\abuenavidah01\Desktop\CE\Sistemas de Big Data Justo\PRACTICA 3 - UD3\PRACTICA 3 - UD3\cripto_data.csv"

        #Guardamos el DataFrame en un archivo CSV 
df_final.to_csv(ruta_destino, index=False)

    #MENSAJE FINAL 
print(f"\n Misión cumplida! Se han guardado {len(df_final)} monedas.")
print(f"Comprueba esta carpeta: {ruta_destino}")

print("\nMuestra de los primeros datos:")
print(df_final.head())