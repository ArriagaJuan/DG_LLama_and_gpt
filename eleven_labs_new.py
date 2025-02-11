import warnings

# Suppress all warnings
warnings.filterwarnings("ignore")

# Your existing imports and code here
import os
from elevenlabs import play, save
from elevenlabs.client import ElevenLabs
import logging

logging.getLogger().setLevel(logging.ERROR)  # Hide warning log

eleven_api_key = os.environ.get('ELEVEN_LABS_KEY')
client = ElevenLabs(api_key=eleven_api_key)

def text_to_audio(text):
    audio = client.generate(
        text=text,
        model="eleven_multilingual_v2",
        voice="IDAS_1"
    )
    #save(audio, "demo.mp3")
    play(audio)



def main():
    
    # Initialize an empty string for the user input
    user_input = ""

    # While loop runs until user_input equals 'q'
    while True:
        user_input = input("\nWrite what you want to hear. Press q to exit: ")
        if user_input.lower() == 'q':
            break

        print(f"{user_input}")

        # Text to audio
        text_to_audio(user_input)


    print("Good bye.")



if __name__ == "__main__":
    main()