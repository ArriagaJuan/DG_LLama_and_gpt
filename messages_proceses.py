import os
import time
import textwrap
import importlib

from setpathtomedia import seleccion
from Setgpt import api_gpt
from labs import text_audio
from load_image import load_input
import utils
import api_utils

# Variables globales para cachear los módulos de Llama
llama1b_module = None
llama3b_module = None

def get_llama1b_response(prompt: str) -> str:
    """
    Carga el módulo llama1b de forma diferida (lazy loading) y obtiene la respuesta.
    Se usa cacheo para que solo se cargue una vez.
    """
    global llama1b_module
    if llama1b_module is None:
        print("Cargando módulo llama1b...")
        llama1b_module = importlib.import_module('llama1b')
    return llama1b_module.ask_Llama1B(prompt)

def get_llama3b_response(prompt: str) -> str:
    """
    Carga el módulo Llama3B de forma diferida (lazy loading) y obtiene la respuesta.
    Se usa cacheo para que solo se cargue una vez.
    """
    global llama3b_module
    if llama3b_module is None:
        print("Cargando módulo Llama3B...")
        llama3b_module = importlib.import_module('Llama3B')
    return llama3b_module.ask_Llama3B(prompt)

def set_character(personaje: str):
    """
    Configura el personaje y la voz correspondiente.
    
    Args:
        personaje (str): Nombre del personaje (por ejemplo, 'Albert' o 'Steve').
        
    Returns:
        tuple: (messages, selected_voice_id, greeting)
            - messages: Estructura de mensajes inicial configurada por api_gpt.
            - selected_voice_id: Identificador de la voz seleccionada.
            - greeting: Cadena de saludo personalizada.
    """
    # Normaliza el nombre (primer letra en mayúscula)
    personaje = personaje.capitalize()

    # Configura la ruta a los medios asociados al personaje
    seleccion(personaje)

    # Configura el sistema de mensajes para el clon digital
    messages = api_gpt(personaje)

    # Configura la voz mediante la API de Eleven Labs (o similar)
    selected_voice_id = text_audio(personaje)

    greeting = f'Hola, soy {personaje}. ¿En qué puedo ayudarte?'
    return messages, selected_voice_id, greeting

def interaction(prompt: str,
                modelo_seleccionado: str,
                selected_voice_id: str,
                input_video_path: str,
                openai_client,
                openai_model: str,
                eleven_api_key: str,
                results_path: str,
                device,
                model) -> str:
    """
    Función principal de interacción que:
      1. Carga el video de entrada.
      2. Selecciona y ejecuta el modelo de lenguaje.
      3. Convierte la respuesta a audio.
      4. Carga el audio.
      5. Anima el video con el audio generado.
      
    Devuelve:
        str: Respuesta generada por el modelo seleccionado.
    """
    start_total = time.time()

    # 1. Cargar fotogramas y fps del video de entrada
    start = time.time()
    try:
        frames, fps = load_input(input_video_path)
    except Exception as e:
        return f"Error al cargar el video: {e}"
    t_load_video = time.time() - start
    print(f"Tiempo para cargar el video: {t_load_video:.2f} segundos")

    if prompt.strip().lower() == 'exit':
        return 'Hasta la próxima'

    # 2. Seleccionar y ejecutar el modelo de lenguaje
    # Normalizamos la cadena a minúsculas para que la comparación sea insensible a mayúsculas/minúsculas
    modelo_opcion = modelo_seleccionado.strip().lower()
    
    # Diccionario de modelos (con claves en minúsculas)
    modelos = {
        "gpt api": lambda: api_utils.get_text_response(openai_client, openai_model, prompt, [])[0],
        "llama 1b": lambda: get_llama1b_response(prompt),
        "llama 3b": lambda: get_llama3b_response(prompt)
    }
    
    start = time.time()
    if modelo_opcion in modelos:
        print(f"Modelo seleccionado: {modelo_seleccionado}")
        try:
            response_text = modelos[modelo_opcion]()
        except Exception as e:
            return f"Error al obtener la respuesta del modelo {modelo_seleccionado}: {e}"
    else:
        return "Modelo no válido seleccionado."
    t_response = time.time() - start
    print(f"Tiempo para generar respuesta: {t_response:.2f} segundos")

    # 3. Convertir la respuesta a audio
    start = time.time()
    try:
        audio_file = api_utils.text_to_audio(eleven_api_key, selected_voice_id, response_text)
    except Exception as e:
        return f"Error al convertir texto a audio: {e}"
    t_text_to_audio = time.time() - start
    print(f"Tiempo para convertir texto a audio: {t_text_to_audio:.2f} segundos")

    # 4. Cargar el audio
    start = time.time()
    try:
        audio, audio_file = utils.load_input_audio(file_path=audio_file, fps=fps, results_path=results_path)
    except Exception as e:
        return f"Error al cargar el audio: {e}"
    t_load_audio = time.time() - start
    print(f"Tiempo para cargar el audio: {t_load_audio:.2f} segundos")

    # 5. Animar el video con el audio generado
    start = time.time()
    try:
        utils.animate_input(frames, audio, audio_file, fps, model, device, results_path)
    except Exception as e:
        return f"Error al animar el video: {e}"
    t_animate_video = time.time() - start
    print(f"Tiempo para animar el video: {t_animate_video:.2f} segundos")

    total_time = time.time() - start_total
    print(f"Tiempo total de ejecución: {total_time:.2f} segundos")

    return response_text


