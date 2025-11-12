#Vamos a conectarnos a DynamoDB 

import boto3

# Crear recurso de DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

# Seleccionar la tabla Orders
table = dynamodb.Table('Orders')

# Confirmar conexión
print(f"Conectado a la tabla '{table.name}' en la región '{dynamodb.meta.client.meta.region_name}'.")



# Función para crear un nuevo pedido
def create_order(order_id, customer_name, product, quantity, status):
    '''Crea un nuevo ítem en la tabla Orders.'''
    try:
        response = table.put_item(
           Item={
                'order_id': order_id,
                'customer_name': customer_name,
                'product': product,
                'quantity': quantity,
                'status': status,
                'order_date': '2025-11-10' # Puedes usar una fecha actual
            }
        )
        print(f"Pedido {order_id} creado exitosamente.")
        return response
    except Exception as e:
        print(f"Error al crear el pedido: {e}")

#llamamos a la función para crear un pedido de ejemplo
create_order('1001', 'Juan Perez', 'Laptop', 1, 'Pending')




# Función para leer un pedido por su ID
def get_order(order_id):
    '''Obtiene un ítem de la tabla Orders por su ID.'''
    try:
        response = table.get_item(Key={'order_id': order_id})
        item = response.get('Item')
        if item:
            print(f"Datos del pedido {order_id}: {item}")
            return item
        else:
            print(f"No se encontró el pedido con ID {order_id}.")
            return None
    except Exception as e:
        print(f"Error al obtener el pedido: {e}")

#llamamos a la función para obtener un pedido de ejemplo
get_order('1001')




# Función para actualizar el estado de un pedido
def update_order_status(order_id, new_status):
    '''Actualiza el atributo 'status' de un pedido.'''
    try:
        response = table.update_item(
            Key={'order_id': order_id},
            UpdateExpression="set #st = :s",
            ExpressionAttributeNames={'#st': 'status'},
            ExpressionAttributeValues={':s': new_status},
            ReturnValues="UPDATED_NEW"
        )
        print(f"Estado del pedido {order_id} actualizado a '{new_status}'.")
        return response
    except Exception as e:
        print(f"Error al actualizar el pedido: {e}")

#llamamos a la función para actualizar el estado de un pedido de ejemplo
update_order_status('1001', 'Shipped')
