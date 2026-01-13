# Práctica 1: Hijo de la Forja (Limpieza de Datos Masivos)
**Autor:** Adrián Buenavida

---

## Descripción de la práctica
El objetivo de esta práctica consiste en desarrollar un script de Python utilizando la librería **pandas** para realizar la limpieza, normalización y validación de un dataset de ventas con más de 15,000 registros. Se han corregido duplicados, errores en precios e inconsistencias en formatos de fecha.

---

## Paso 1: Carga del dataset y análisis inicial
En este primer paso, realizamos la carga del archivo `.csv` y utilizamos el método `info()` para observar la estructura original y detectar columnas con valores nulos o tipos de datos incorrectos.

**Código utilizado:**
```python
df = pd.read_csv('ventas_big_data_ut3.csv')
print(df.info())
```

