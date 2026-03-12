import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
tabla = dynamodb.Table('CensoAlianza')

def insertar_registros():
    try:
        # Registro 1: Básico
        tabla.put_item(Item={
            'ID_Ninja': 'N001',
            'Nombre': 'Naruto Uzumaki',
            'Clan': 'Uzumaki',
            'Rango': 'Hokage'
        })

        # Registro 2: Estructura flexible (Array y JSON)
        tabla.put_item(Item={
            'ID_Ninja': 'N002',
            'Nombre': 'Sasuke Uchiha',
            'Habilidades': ['Sharingan', 'Rinnegan'],
            'Equipamiento': {'Arma': 'Kusanagi', 'Accesorio': 'Capa'}
        })

        # Registro 3: Diferentes atributos
        tabla.put_item(Item={
            'ID_Ninja': 'N003',
            'Nombre': 'Kakashi Hatake',
            'Ultima_Mision': 'Rango S - Éxito'
        })

        print("¡Registros insertados en DynamoDB con éxito!")
    except Exception as e:
        print(f"Error al conectar con DynamoDB: {e}")

if __name__ == "__main__":
    insertar_registros()