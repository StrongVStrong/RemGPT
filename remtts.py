import requests
import pygame
import io
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize pygame mixer for audio playback
pygame.mixer.init()

api_key = os.getenv("Papi_key") #Enter your PlayHT API key here/your .env file
user_id = os.getenv("user_id") #Enter your PlayHT user ID here/your .env file

# Cloned voice ID from the response
voice_id = "s3://voice-cloning-zero-shot/4bdadb2c-51b5-43a6-a4f9-68d251d2f238/original/manifest.json"

# PlayHT API URL for TTS Streaming
url = "https://api.play.ht/api/v2/tts/stream"

# Headers for authentication
headers = {
    "Authorization": f"Bearer {api_key}",
    "X-User-Id": user_id 
}
pygame.mixer.init()

def gen_audio(text):
    # Parameters for TTS
    params = {
        "text": text,
        "voice": voice_id,  # Use the cloned voice ID here
        "output_format": "mp3",  # You can change the format if needed
        "speed": 1.0,  # Adjust the speed of speech
        "sample_rate": 22050,  # Adjust sample rate if needed
    }

    # Send POST request to generate speech
    response = requests.post(url, headers=headers, json=params)

    # Check the response
    if response.status_code == 200:
        # Use io.BytesIO to load the audio content directly into pygame
        audio_data = io.BytesIO(response.content)
        
        # Load the audio into pygame mixer
        pygame.mixer.music.load(audio_data, "mp3")
        
        # Play the audio
        pygame.mixer.music.play()

        # Wait until the audio is finished playing
        while pygame.mixer.music.get_busy():  # Check if music is still playing
            pygame.time.Clock().tick(10)
    else:
        print(f"Error generating speech: {response.status_code} - {response.text}")
