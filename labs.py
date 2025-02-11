import elevenlabs as elevlabs

def text_audio(eleven_api_key=None,clone_to_use='Albert', verbose=False):

    # Configure GPT and Text-to-speech API keys
    elevlabs.set_api_key(eleven_api_key)

    # Configure voice
    # Configurar las voces disponibles
    voice_list = elevlabs.voices()
    voice_labels = [voice.category + " voice: " + voice.name for voice in voice_list]

    if verbose:
        print("Existing voices:")
        for label in voice_labels:
            print(label)

    # Seleccionar la voz a usar
    if clone_to_use == "Steve":
        voice_id = f"cloned voice: Steve"
    elif clone_to_use == "Albert":
        voice_id = f"generated voice: Albert"
    else:
        raise ValueError(f"No voice configuration found for: {clone_to_use}")
    try:
        selected_voice_index = voice_labels.index(voice_id)
    except ValueError:
        raise ValueError(f"Voice '{voice_id}' not found in available voices.")

    selected_voice_id = voice_list[selected_voice_index].voice_id

    if verbose:
        print(f"\nSelected voice: {voice_id}")

    return selected_voice_id