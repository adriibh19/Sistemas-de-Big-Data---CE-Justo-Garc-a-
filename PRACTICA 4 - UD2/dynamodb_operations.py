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
#create_order('1001', 'Juan Perez', 'Laptop', 1, 'Pending')




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
#get_order('1001')




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
#update_order_status('1001', 'Shipped')



# Función para eliminar un pedido por su ID
def delete_order(order_id):
    '''Elimina un ítem de la tabla Orders.'''
    try:
        response = table.delete_item(Key={'order_id': order_id})
        print(f"Pedido {order_id} eliminado exitosamente.")
        return response
    except Exception as e:
        print(f"Error al eliminar el pedido: {e}")

#llamamos a la función para eliminar un pedido de ejemplo
#delete_order('1001')



# Función para buscar pedidos por nombre de cliente
from boto3.dynamodb.conditions import Attr

def get_orders_by_customer(customer_name):
    """Devuelve todos los pedidos realizados por un cliente concreto."""
    try:
        response = table.scan(
            FilterExpression=Attr('customer_name').eq(customer_name)
        )
        items = response.get('Items', [])
        
        if items:
            print(f"Pedidos de {customer_name}:")
            for item in items:
                print(item)
        else:
            print(f"No se encontraron pedidos para el cliente {customer_name}.")
        
        return items
    except Exception as e:
        print(f"Error al buscar pedidos por cliente: {e}")


#llamamos a la función para buscar pedidos por cliente de ejemplo
#get_orders_by_customer("Javier Ruiz")



#implementamos la sentencia del main para la demostración
if __name__ == "__main__":
    print("\n Demostración de operaciones con DynamoDB \n")

    #1.Creamos un nuevo pedido
    create_order("ORD-PY-1001", "Javier Ruiz", "Teclado Mecánico", 1, "Pending")

    #2.Leemos el pedido recién creado
    get_order("ORD-PY-1001")

    #3.Actualizamos su estado
    update_order_status("ORD-PY-1001", "Shipped")
    get_order("ORD-PY-1001")  # Verificamos el cambio

    #4 Buscamos todos los pedidos de un cliente (usa un nombre que exista en tu tabla)
    get_orders_by_customer("Javier Ruiz")
    get_orders_by_customer("Carlos Soto")  # Ejemplo con otro cliente

    #5.Eliminamos el pedido
    delete_order("ORD-PY-1001")
    get_order("ORD-PY-1001")  # Verificamos que ya no existe

    print("\n Demostración finalizada \n")


    #como comentario destacado, he de explicar que he comentado todas las llamadas a las funciones para que no me diera error ya que se van a ejecutar a última hora