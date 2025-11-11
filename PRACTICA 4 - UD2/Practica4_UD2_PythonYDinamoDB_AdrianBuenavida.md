# Práctica 4: Práctica 4: Automatización de DynamoDB con Python y Boto3_AdrianBuenavida


## 1a PARTE: Preparamos el entorno

### 1.1 Configuramos AWScli 

Dentro de AWSAcademy, vamos arriba a la derecha, alapartado de "AWS Details" y hacemos click. Nos aparecerán unos datos relacionados con nuestro usuario.

Luego vamos al cmd y escribimos "aws configuration", y comenzamo con la configuración.

#### Comprobación
![ Comprobacion ](./imagenes/3.png)




### 1.2 Instalamos Python y Pip

#### Comprobación - Python
![ Comprobacion](./imagenes/instalacion_python.png)


#### Comprobación - Boto3
![ Comprobacion](./imagenes/boto3.png)


### 1.3. Verificación de las Credenciales

Escribimos en el cmd el siguiente comando: ```aws sts get-caller-identity```

#### Comprobación
![ Comprobacion](./imagenes/4.png)


<br>

## 2a PARTE: Automatizando Operaciones con Boto3

