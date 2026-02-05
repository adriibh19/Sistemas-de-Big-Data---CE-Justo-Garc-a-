# Práctica 3: Extracción de datos en CoinMarketCap (Web Scraping)
**Autor:** Adrián Buenavida

## Descripción de la práctica
En esta práctica, vamos a realizar una extracción de datos en un entorno no estructurado. 

Aquí debemos navegar por el DOM de la web de CoinMarketCap para "leer" la información de las 500 principales criptomonedas y almacenarlas para su análisis

---

## Paso 1: Configuramos acceso y bloqueos
Dado que CoinMarketCap protege sus datos frente a accesos automatizados, hemos tenido que preparar nuestra petición para que " parezca humana"



**estrategia:**

1. **User-Agent:** Hemos incluido una cabecera (`headers`) en la que simulamso la navegación desde un navegador Chrome estándar, evitando que el servidor bloquee nuestra IP al detectarnos como un script de Python, que es lo que hemos hecho

2. **BeautifulSoup:** Una vez obtenida la respuesta del servidor, utilizamos el motor de `BeautifulSoup` para transformar el HTML crudo en un objeto navegable (he buscado inform en internet)

3. **Localización de las filas:** Hemos identificado que los datos residen en una tabla con la clase `cmc-table`. Mediante selectores CSS, localizamos todas las etiquetas `<tr>` que contienen la información de cada activo



**Código utilizado:**
```python
headers = {'User-Agent': 'Mozilla/5.0 ... Chrome/119.0.0.0 ...'}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')
filas = soup.select('table.cmc-table tbody tr')
```

![ Captura1](./imagenes/1.png)

<br>


## Paso 2: Analizamos el del DOM y extracción de atributos
Una vez establecida la conexión, nuestro objetivo ha sido identificar la ubicación exacta de los datos dentro de la estructura de la tabla.

**estrategia:**

1. **Filas:** Hemos recorrido cada etiqueta `<tr>` obtenida, descartando aquellas que no cumplen con el número mínimo de celdas para evitar filas que no nos sirven como las de publicidad 

2. **Localizamos índice:** Mediante `find_all('td')`, hemos accedido a las columnas específicas donde CoinMarketCap almacena el nombre, el precio actual, la capitalización de mercado y el volumen de transacciones

3. **Almacenamiento temporal:** Los datos se han estructurado en una lista de diccionarios, paso muy importyante para su posterior transformación y limpieza con la librería pandas

**Código utilizado:**
```python
for fila in filas:
    celdas = fila.find_all('td')
    if len(celdas) > 5:
        nombre = celdas[2].text.strip()
        precio = celdas[3].text.strip()
```

![ Captura2](./imagenes/2.png)




<br>

## Paso 3: Escalabilidad y Paginación
Para c obtener 500 registros, he automatizado la navegación por las distintas páginas de CoinMarketCap, gestionando la carga de datos que realiza la web

**estrategia:**

1. **Bucle Iterativo:** He configurado un  `for` que recorre de la página 1 a la 5, inyectando el número de página dinámicamente en la URL para capturar 100 registros por parada

2. **Código:** He implementado bloques `try/except` y validaciones de longitud de celdas para evitar errores de tipo `IndexError`. Esto permite que, si una fila tiene una estructura diferente o incompleta, el script asigne valores "N/A" y continúe sin detenerse

3. **Tiempos (Sleep):** He aplicado un `time.sleep(2)` entre cada petición para simular un comportamiento humano y evitar que los sistemas de seguridad de la web bloqueen mi dirección IP

![ Captura3](./imagenes/3.png)




<br>

## Paso 4: Almacenamiento y Persistencia
Finalmente, he utilizado la librería **Pandas** para consolidar toda la información capturada en una lista de diccionarios y exportarla a un archivo CSV estructurado.

**Código utilizado:**
```python
df_final = pd.DataFrame(lista_criptos)
df_final.to_csv("cripto_data.csv", index=False)
```

![ Captura4](./imagenes/4.png)



<br>


## Paso 5: Limpieza de datos
Los datos extraídos directamente de la web venían con símbolos de dólar ("$") y comas que impedían tratarlos como valores numéricos 

**estrategia:**

1. **Eliminación de caracteres:** He aplicado los métodos `.replace('$', '')` y `.replace(',', '')` a los campos de Precio, Market Cap y Volumen para limpiar los textos y convertirlos en números reales

2. **Filtrado:** He implementado un filtro final en el DataFrame para descartar aquellas filas que no contenían nombres válidos o que daban errores de "NaN" debido a los encabezados de la tabla o campos publicitarios

**Código utilizado:**
```python
# Paso 5: Limpiamos los datos de símbolos y comas #taltaltal
precio = celdas[3].text.replace('$', '').replace(',', '').strip()
market_cap = celdas[7].text.replace('$', '').replace(',', '').strip()

# filtramos filas que no tienen nombre para evitar NaNs #taltaltal
df_final = df_final[df_final['Nombre'] != "N/A"].drop_duplicates()
```

![ Captura5](./imagenes/5.png)


**Comprobación de la creación del .csv:**

![ Captura5](./imagenes/6.png)