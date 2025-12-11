from flask import Flask, jsonify, request
import boto3
from boto3.dynamodb.conditions import Key, Attr
from flask_cors import CORS 
from decimal import Decimal 

# --- 1. CONFIGURACIÓN DE AWS DYNAMODB ---

AWS_REGION = 'us-east-1' 
DYNAMODB = boto3.resource('dynamodb', region_name=AWS_REGION)

# Tablas (los nombres deben coincidir exactamente)
INVENTORY_TABLE = DYNAMODB.Table('CInventory')
USERS_TABLE = DYNAMODB.Table('CUsers')
SALES_TABLE = DYNAMODB.Table('CSales') 

# Nombres de los GSIs
STATUS_PRICE_GSI = 'StatusPriceIndex' 
ROLE_INDEX_GSI = 'RoleIndex' 

# --- 2. CONFIGURACIÓN DE FLASK ---
app = Flask(__name__)
# Habilitar CORS para permitir que la web (file:///) se conecte a la API (http://127.0.0.1:5000)
CORS(app) 

# --- ENDPOINT DE PRUEBA ---
@app.route('/', methods=['GET'])
def home():
    """Endpoint de prueba."""
    return jsonify({
        "status": "API REST Concesionario Fénix OK",
        "message": "Usa /vehicles/available para la Consulta Obligatoria."
    })

# ==============================================================================
# 4.1. CONSULTA COMPLEJA OBLIGATORIA (CInventory)
# ==============================================================================

@app.route('/vehicles/available', methods=['GET'])
def get_available_vehicles():
    """
    Objetivo: Obtener todos los vehículos DISPONIBLES y ordenados por precio (de menor a mayor).
    Implementación: Usando QUERY sobre el GSI StatusPriceIndex.
    """
    try:
        response = INVENTORY_TABLE.query(
            IndexName=STATUS_PRICE_GSI,
            KeyConditionExpression=Key('Filtro_1_PK').eq('STATUS#Disponible')
        )
        
        vehicles = response.get('Items', [])
        
        return jsonify({
            "count": len(vehicles),
            "vehicles": vehicles
        })

    except Exception as e:
        print(f"Error al ejecutar la Consulta Compleja: {e}")
        return jsonify({
            "error": "Error de conexión o configuración del GSI/Tabla.",
            "details": str(e)
            }), 500


# ==============================================================================
# 4.2. ENDPOINTS CRUD ESTÁNDAR PARA CInventory
# ==============================================================================

# A. GET /vehicles (Listar TODOS los datos - Requisito CRUD Básico)
@app.route('/vehicles', methods=['GET'])
def list_all_vehicles():
    """
    Objetivo: Listar TODOS los vehículos en el inventario.
    Implementación: Usando Scan.
    """
    try:
        response = INVENTORY_TABLE.scan()
        
        vehicles = response.get('Items', [])
        
        return jsonify({
            "count": len(vehicles),
            "vehicles": vehicles
        })

    except Exception as e:
        print(f"Error al listar todos los vehículos: {e}")
        return jsonify({"error": "Error interno del servidor o de la BD."}), 500


# B. GET /vehicles/{id} (READ específico)
@app.route('/vehicles/<string:vin>', methods=['GET'])
def get_vehicle_by_vin(vin):
    """
    Objetivo: Obtener los detalles de un vehículo usando su VIN.
    Implementación: Usando GetItem. Devuelve 404 si no existe.
    """
    try:
        response = INVENTORY_TABLE.get_item(
            Key={
                'PK': f'VEHICLE#{vin}',
                'SK': f'DETAILS#{vin}'
            }
        )
        
        item = response.get('Item')
        
        if not item:
            return jsonify({"message": f"Vehículo con VIN {vin} no encontrado."}), 404
        
        return jsonify(item)

    except Exception as e:
        print(f"Error al obtener el vehículo: {e}")
        return jsonify({"error": "Error interno del servidor o de la BD."}), 500


# C. POST /vehicles (CREATE)
@app.route('/vehicles', methods=['POST'])
def create_vehicle():
    """
    Objetivo: Crear un nuevo vehículo en la tabla CInventory.
    Implementación: Usando PutItem.
    """
    try:
        data = request.get_json()
        
        if not all(k in data for k in ["VIN", "Marca", "Modelo", "Precio", "Kilometraje", "Estado"]):
            return jsonify({"error": "Faltan campos obligatorios (VIN, Marca, Modelo, Precio, Kilometraje, Estado)."}), 400

        vin = data['VIN']
        estado = data['Estado']
        
        #Conversión a Decimal para evitar errores de precisión de Float
        precio = Decimal(str(data['Precio'])) 
        kilometraje = Decimal(str(data['Kilometraje']))

        item = {
            'PK': f'VEHICLE#{vin}',
            'SK': f'DETAILS#{vin}',
            'Filtro_1_PK': f'STATUS#{estado}', 
            'Filtro_1_SK': precio,             
            'VIN': vin,
            'Marca': data['Marca'],
            'Modelo': data['Modelo'],
            'Precio': precio,                   
            'Estado': estado,
            'Kilometraje': kilometraje          
        }

        INVENTORY_TABLE.put_item(Item=item)
        
        return jsonify({"message": "Vehículo creado con éxito", "VIN": vin}), 201

    except Exception as e:
        print(f"Error al crear el vehículo: {e}")
        return jsonify({"error": "Error interno del servidor o de la BD.", "details": str(e)}), 500


# D. PUT /vehicles/{id} (UPDATE)
@app.route('/vehicles/<string:vin>', methods=['PUT'])
def update_vehicle(vin):
    """
    Objetivo: Actualizar atributos de un vehículo existente.
    Implementación: Usa UpdateItem.
    """
    try:
        data = request.get_json()
        
        key = {
            'PK': f'VEHICLE#{vin}',
            'SK': f'DETAILS#{vin}'
        }

        update_expression = "SET"
        expression_attribute_values = {}
        
        if 'Marca' in data:
            update_expression += " Marca = :m,"
            expression_attribute_values[':m'] = data['Marca']
        if 'Modelo' in data:
            update_expression += " Modelo = :o,"
            expression_attribute_values[':o'] = data['Modelo']

        # Tipado corregido: Kilometraje debe ser Decimal
        if 'Kilometraje' in data: 
            kilometraje = Decimal(str(data['Kilometraje']))
            update_expression += " Kilometraje = :k,"
            expression_attribute_values[':k'] = kilometraje
            
        # Tipado corregido: Precio debe ser Decimal (actualiza GSI)
        if 'Precio' in data:
            precio = Decimal(str(data['Precio']))
            update_expression += " Precio = :p, Filtro_1_SK = :p_sk," 
            expression_attribute_values[':p'] = precio
            expression_attribute_values[':p_sk'] = precio

        # Estado (actualiza GSI)
        if 'Estado' in data:
            estado = data['Estado']
            update_expression += " Estado = :e, Filtro_1_PK = :e_pk,"
            expression_attribute_values[':e'] = estado
            expression_attribute_values[':e_pk'] = f'STATUS#{estado}'


        if update_expression.endswith(','):
            update_expression = update_expression[:-1]
            
        if update_expression == "SET":
             return jsonify({"message": "No hay atributos para actualizar."}), 400

        INVENTORY_TABLE.update_item(
            Key=key,
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="UPDATED_NEW"
        )
        
        return jsonify({"message": f"Vehículo {vin} actualizado con éxito."}), 200

    except Exception as e:
        print(f"Error al actualizar el vehículo: {e}")
        return jsonify({"error": "Error interno del servidor o de la BD.", "details": str(e)}), 500


# E. DELETE /vehicles/{id} (DELETE)
@app.route('/vehicles/<string:vin>', methods=['DELETE'])
def delete_vehicle(vin):
    """
    Objetivo: Eliminar un vehículo de la tabla CInventory.
    Implementación: Usando DeleteItem.
    """
    try:
        key_to_delete = {
            'PK': f'VEHICLE#{vin}',
            'SK': f'DETAILS#{vin}'
        }
        
        response = INVENTORY_TABLE.delete_item(
            Key=key_to_delete,
            ReturnValues='ALL_OLD'
        )
        
        if not response.get('Attributes'):
            return jsonify({"message": f"Vehículo con VIN {vin} no encontrado."}), 404

        return jsonify({"message": f"Vehículo {vin} eliminado con éxito."}), 200

    except Exception as e:
        print(f"Error al eliminar el vehículo: {e}")
        return jsonify({"error": "Error interno del servidor o de la BD.", "details": str(e)}), 500


# ==============================================================================
# 4.3. CONSULTA ADICIONAL (CUsers)
# ==============================================================================

@app.route('/users/role/<string:role_name>', methods=['GET'])
def get_users_by_role(role_name):
    """
    Objetivo: Obtener todos los empleados con un rol específico (ej. Comercial).
    Implementación: Usando QUERY sobre el GSI RoleIndex en la tabla CUsers.
    """
    try:
        partition_key_value = f'ROLE#{role_name}' 
        
        response = USERS_TABLE.query(
            IndexName=ROLE_INDEX_GSI,
            KeyConditionExpression=Key('Filtro_1_PK').eq(partition_key_value)
        )
        
        users = response.get('Items', [])
        
        return jsonify({
            "role": role_name,
            "count": len(users),
            "employees": users
        })

    except Exception as e:
        print(f"Error al obtener usuarios por rol: {e}")
        return jsonify({"error": "Error interno del servidor o de la BD.", "details": str(e)}), 500


# --- INICIAR LA APLICACIÓN ---
if __name__ == '__main__':
    # Ejecuta la aplicación en modo debug
    app.run(debug=True, port=5000)