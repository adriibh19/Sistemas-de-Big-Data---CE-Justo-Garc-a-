# Proyecto 1er trimestre: "Gestión de Inventario para Concesionario de Coches"
## Autores: Adrián Buenavida y José Luis Saavedra

---

## 1. Modelado de un Problema de Negocio Real

### 1.1. Definición del Problema

El proyecto elegido, aborda la **Gestión de inventario y ventas** para un concesionario de coches. 

El problema se centra en garantizar el **acceso rápido** a la información detallada de cada vehículo por su identificador único (**VIN**), y permitir **consultas eficientes por filtros** clave (como obtener todos los coches **disponibles** ordenados por **precio**).

La naturaleza del problema requiere una BD que priorice la **velocidad de lectura por clave** y la **escalabilidad horizontal** frente a la complejidad relacional, haciendo de DynamoDB la elección óptima.


<br>


### 1.2. Modelado de Datos (Esquema y Claves)

Hemos optado por un diseño de **3 tablas** (`CInventory`, `CSales`, `CUsers`) utilizando el modelo de diseño de **"claves compuestas"** y **GSI (Índices Secundarios Globales)** para resolver todos los patrones de acceso con la máxima eficiencia.


<br>

#### Estructura de la 3 tablas `CInventory`, `CSales`, `CUsers`

Hemos usado la web de draw.io para realizar el esquema a modo generald e cómo vamos a estructurar nuestro proyecto

![ Comprobacion del ej 1](./imagenes/diagrama.png)



Y ahora, creamos las 3 tablas en AWS:
 

a) `CInventory`

Comando usado: 
```python
aws dynamodb create-table \
    --table-name CInventory \
    --attribute-definitions \
        AttributeName=PK,AttributeType=S \
        AttributeName=SK,AttributeType=S \
        AttributeName=Filtro_1_PK,AttributeType=S \
        AttributeName=Filtro_1_SK,AttributeType=N \
    --key-schema \
        AttributeName=PK,KeyType=HASH \
        AttributeName=SK,KeyType=RANGE \
    --billing-mode PAY_PER_REQUEST \
    --global-secondary-indexes '[{"IndexName":"StatusPriceIndex","KeySchema":[{"AttributeName":"Filtro_1_PK","KeyType":"HASH"},{"AttributeName":"Filtro_1_SK","KeyType":"RANGE"}],"Projection":{"ProjectionType":"ALL"}}]'
```


b)`CSales`

Comando usado: 
```python
aws dynamodb create-table 
    --table-name CSales 
    --attribute-definitions AttributeName=PK,AttributeType=S AttributeName=SK,AttributeType=S 
    --key-schema AttributeName=PK,KeyType=HASH AttributeName=SK,KeyType=RANGE 
    --billing-mode PAY_PER_REQUEST
```


c)`CUsers`

Comando usado: 
```python
aws dynamodb create-table 
    --table-name CUsers 
    --attribute-definitions AttributeName=PK,AttributeType=S AttributeName=SK,AttributeType=S AttributeName=Filtro_1_PK,AttributeType=S 
    --key-schema AttributeName=PK,KeyType=HASH AttributeName=SK,KeyType=RANGE 
    --billing-mode PAY_PER_REQUEST 
    --global-secondary-indexes '[{"IndexName":"RoleIndex","KeySchema":[{"AttributeName":"Filtro_1_PK","KeyType":"HASH"}],"Projection":{"ProjectionType":"ALL"}}]'
```

<br>

##### Comprobación de las tres tablas creadas:

![ Comprobacion](./imagenes/3tablascreadas.png)


<br>

### 1.3. Volumen de Datos

Vamos a insertar :


- **50 registros** simulados en la tabla `CInventory`,
esta tabla como tiene bastantes registros, lo que hemos hecho desde la Cloudshell , es hacer un **nano inventory_data.json** y hemos creado un archivo .json en que hemos incluido los 55 registros.

Ahora, solo ejecutamos el siguiente comando...

##### Comando usado
```python
aws dynamodb batch-write-item --request-items file://inventory_data.json
```

##### Comprobación:
![ Comprobacion](./imagenes/codigo_inseercc_cinventory.png)


Usamos un count para que nos devuelva cuantos elementos tenemos. El código es:
```python
aws dynamodb scan --table-name CInventory --select COUNT
```

##### Comprobación:
![ Comprobacion](./imagenes/insercc_completa_cinventory.png)


<br>


- **10 elementos** en `CSales`. También hemos creado un archivo .json para poder incluir todos los elementos directamente
##### Comando usado
```python
aws dynamodb batch-write-item --request-items file://sales.json
```

##### Comprobación:
![ Comprobacion](./imagenes/codigo_inseercc_10_sales.png)


Hacemos el COUNT para la comprobación extra de que se han importado correctamente

##### Comprobación:
![ Comprobacion](./imagenes/insercc_completa_sales.png)



<br>


- **5 elementos** en `CUsers`. Volvemos a crear un nuevo json : users.json para poder incluir todos los elementos.

##### Comando usado
```python
aws dynamodb batch-write-item --request-items file://users.json
```

##### Comprobación:
![ Comprobacion](./imagenes/codigo_insercc_5_usuarios.png)

De nuevo, hacemos el COUNT para que nos cuente en total los elementos que hay en la tabla users, en este caso.

##### Comprobación:
![ Comprobacion](./imagenes/insercc_completa_users.png)



<br>


### Comprobaciones gráficas de la creación de todas las tablas con todos sus elementos:
![ Comprobacion](./imagenes/comprobac_grafica_inventory.png)

![ Comprobacion](./imagenes/comprobac_grafica_sales.png)

![ Comprobacion](./imagenes/comprobac_grafica_userspng.png)






---

## 2. Análisis y Justificación de la Base de Datos

### 2.1. Elección de la Tecnología

* **Base de datos elegida:** **AWS (DynamoDB)**
* **Modelo de Datos:** **Clave-Valor**

### 2.2. Documentación Técnica

* **Modelo de Datos:** DynamoDB es una BD **Clave-Valor sin esquema**. Los datos se almacenan como *Ítems* (sin columnas fijas) identificados por su *Clave Primaria* (compuesta por PK y SK)
<br>

* **Lenguaje de Consulta:** Utiliza una **API** de comandos (ej. `GetItem`, `PutItem`, `Query`).
<br>

* **Características Clave:**
    * **Serverless y Escalabilidad:** AWS gestiona automáticamente el escalado de lectura/escritura (Escalado Horizontal)
    * **GSI (Índices secundarios globales):** Permiten consultas flexibles y eficientes que no usan la clave principal.


### 2.3. Justificación de Superioridad

El modelo de DynamoDB es el más adecuado para el inventario de un concesionario, superando a los otros modelos.... :

1.  **Frente a MongoDB (Documentos):** El inventario de coches tiene atributos estandarizados. DynamoDB, al estar optimizado para el **acceso directo por clave**, ofrece una **velocidad de lectura (Get/Query) superior** que MongoDB.
<br>

2.  **Frente a Neo4j (Grafos):** El problema no requiere analizar **relaciones complejas** (ej. análisis de redes). La tarea principal es **recuperar el ítem por ID (VIN)** y **filtrar listas ordenadas**, para lo cual el modelo Clave-Valor de DynamoDB es **más rápido** que un modelo de Grafos.

---


## 3. Desarrollo de la API para nuestro concesionario

### 3.1. ¿Por qué hemos elegido Python/Flask y Boto3?

Hemos optado por Python (Flask) y la librería Boto3 porque creemos que es la combinación más eficiente para el proyecto:

- **Simplicidad**: Flask nos permite implementar la API REST con el código mínimo necesario.

- **Velocidad**: Python es ideal para el desarrollo rápido.

- **Integración**: Boto3 es el SDK oficial de AWS, lo que garantiza la forma más directa  de conectar la API con nuestra base de datos DynamoDB.

### 3.2 Desarrollo de la API REST
#### 3.2.1 Configuración Inicial del Entorno

Para empezar el desarrollo en Python, debemos configurar el entorno e instalar las dependencias necesarias.

*Pasos a seguir en la CloudShell en **AWS***:

- Crear y Activar el Entorno Virtual.

- Instalar Flask (el framework web minimalista).

- Instalar Boto3 (la librería de AWS para interactuar con DynamoDB)