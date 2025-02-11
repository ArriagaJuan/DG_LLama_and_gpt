import firebase_admin
from firebase_admin import credentials, firestore, storage
from datetime import datetime, timedelta

def subir_firebase(results_path):
    
    if not firebase_admin._apps:
        # Inicializar la aplicación Firebase
        cred = credentials.Certificate('credenciales/credenciales.json')
        firebase_admin.initialize_app(cred, {'storageBucket': 'mentores-c1064.appspot.com'})


    # Inicializa Firestore
    db = firestore.client()
    coleccion_ref = db.collection('Pruebas')

    # Lógica para subir el archivo y obtener la URL con token
    archivo_ruta = results_path.lstrip('./')
    bucket = storage.bucket()
    blob = bucket.blob(archivo_ruta)
    blob.upload_from_filename(archivo_ruta)
    hora_expiracion = datetime.utcnow() + timedelta(minutes=5)
    token = blob.generate_signed_url(expiration=hora_expiracion, method='GET')
    archivo_url_con_token = token

    datos = {
        'archivo_url': archivo_url_con_token,
        # Agrega más campos según sea necesario
    }
    coleccion_ref.add(datos)

    # Imprime la respuesta
    return archivo_url_con_token