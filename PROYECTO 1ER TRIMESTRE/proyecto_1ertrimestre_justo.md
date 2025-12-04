# Proyecto 1er trimestre: "Gestión de Inventario para Concesionario de Coches"
## Autores: Adrián Buenavida y José Luis Saavedra

---

## 1. Modelado de un Problema de Negocio Real

### 1.1. Definición del Problema

El proyecto elegido, aborda la **Gestión de inventario y ventas** para un concesionario de coches. 

El problema se centra en garantizar el **acceso rápido** a la información detallada de cada vehículo por su identificador único (**VIN**), y permitir **consultas eficientes por filtros** clave (como obtener todos los coches **disponibles** ordenados por **precio**).

La naturaleza del problema requiere una BD que priorice la **velocidad de lectura por clave** y la **escalabilidad horizontal** frente a la complejidad relacional, haciendo de DynamoDB la elección óptima.


### 1.2. Modelado de Datos (Esquema y Claves)

Hemos optado por un diseño de **3 tablas** (`CInventory`, `CSales`, `CUsers`) utilizando el modelo de diseño de **"claves compuestas"** y **GSI (Índices Secundarios Globales)** para resolver todos los patrones de acceso con la máxima eficiencia.


#### Estructura de la 3 tablas `CInventory`, `CSales`, `CUsers`

Hemos usado la web de draw.io para realizar el esquema a modo generald e cómo vamos a estructurar nuestro proyecto

![ Comprobacion del ej 1](./imagenes/diagrama.png)




### 1.3. Volumen de Datos

Se generarán e insertarán un mínimo de **50 registros** simulados en la tabla `ConcesionarioInventory`. Esto incluye la simulación de coches con el `Estado` **'Disponible'** (para probar la Consulta Compleja) y **'Vendido'** (para demostrar la gestión de inventario).

---

## 2. Análisis y Justificación de la Base de Datos

### 2.1. Elección de la Tecnología

* **Tecnología Elegida:** **Amazon DynamoDB**
* **Modelo de Datos:** **Clave-Valor / Columnar Amplia.**

### 2.2. Documentación Técnica

* **Modelo de Datos:** DynamoDB es una BD **Clave-Valor Sin Esquema (Schema-less)**. Los datos se almacenan como *Ítems* (sin columnas fijas) identificados por su *Clave Primaria* (compuesta por PK y SK).
* **Lenguaje de Consulta:** Utiliza una **API** de comandos (ej. `GetItem`, `PutItem`, `Query`).
* **Características Clave:**
    * **Rendimiento Garantizado:** **Latencia de milisegundos de un solo dígito** constante.
    * **Serverless y Escalabilidad:** AWS gestiona automáticamente el escalado de la capacidad de lectura/escritura (Escalado Horizontal).
    * **GSI (Índices Secundarios Globales):** Permiten consultas flexibles y eficientes que no usan la clave principal.

### 2.3. Justificación de Superioridad

El modelo de DynamoDB es el más adecuado para el inventario de un concesionario, superando a los otros modelos:

1.  **Frente a MongoDB (Documentos):** El inventario de coches tiene atributos estandarizados. DynamoDB, al estar optimizado para el **acceso directo por clave**, ofrece una **velocidad de lectura (Get/Query) superior y más predecible** que MongoDB.
2.  **Frente a Neo4j (Grafos):** El problema no requiere analizar **relaciones complejas** (ej. análisis de redes). La tarea principal es **recuperar el ítem por ID (VIN)** y **filtrar listas ordenadas**, para lo cual el modelo Clave-Valor de DynamoDB es **más rápido y rentable** que un modelo de Grafos.

---