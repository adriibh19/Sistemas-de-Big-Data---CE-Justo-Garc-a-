# Práctica 1 - UD3: Hijo de la Forja (Limpieza de Datos Masivos)
**Autor:** Adrián Buenavida

## Descripción de la práctica
Esta práctica realizaremos un proceso de limpieza sobre un dataset de 15,451 registros. El objetivo es asegurarnos que la información esté estructurada antes de su procesamiento

---

## Paso 1: Carga del dataset y análisis inicial
En esta fase, utilizamos la librería **pandas** para cargar el archivo CSV y realizar unas "consultas" de su estructura mediante el método `info()`

**Observaciones de la carga de datos:**
* Se cargaron un total de **15,451 entradas**.
* La columna `precio` tiene valores nulos (14,677 no nulos), teniendo también presencia de errores como cadenas "ERR".
* Las columnas `fecha`, `producto` y `precio` son tratadas inicialmente como objetos (strings), lo que posteriormente, tendremos que tratarlas.

**Código utilizado:**
```python
df = pd.read_csv('ventas_big_data_ut3.csv')
print(df.info())
```

![ Captura](./imagenes/1.png)


<br>

## Paso 2: Fase de Limpieza estructural
En esta etapa se han corregido las inconsistencias de la estructura del dataset sin perder volumen de información innecesariamente.


**Qué hemos hecho:**

1. **Eliminación de duplicados:** Detectamos y eliminamos **451** registros igueles mediante `drop_duplicates()`
2. **Tratamiento de Cantidades Negativas:** Identificamos **298** registros con valores negativos. Así pues, calculamos la mediana de los valores positivos (siendo **6.0**) y la aplicamos para corregir dichos errores 
3. **Integridad de datos:** El uso de `.copy()` nos permite que `df_paso2` funcione como un objeto independiente, evitando conflictos de memoria en las siguientes transformaciones.

**Código utilizado:**
```python
mediana_cantidad = df_sin_duplicados.loc[df_sin_duplicados['cantidad'] >= 0, 'cantidad'].median()
df_sin_duplicados.loc[df_sin_duplicados['cantidad'] < 0, 'cantidad'] = mediana_cantidad
df_paso2 = df_sin_duplicados.copy()
```

![ Captura](./imagenes/2.png)