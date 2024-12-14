import requests
import pygame
import io
import os
from dotenv import load_dotenv
import tempfile

load_dotenv()

# Initialize pygame mixer for audio playback
pygame.mixer.init()

api_key = os.getenv("Papi_key")  # Enter your PlayHT API key here/your .env file
user_id = os.getenv("user_id")   # Enter your PlayHT user ID here/your .env file

# Cloned voice ID from the response
voice_id = "s3://voice-cloning-zero-shot/3cfcb7b6-8083-40ed-81d7-841f880b560c/original/manifest.json"

# PlayHT API URL for TTS Streaming
url = "https://api.play.ht/api/v2/tts/stream"

# Headers for authentication
headers = {
    "Authorization": f"Bearer {api_key}",
    "X-User-Id": user_id
}

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
        # Create a temporary file to save the audio data
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        
        # Save the audio data to the temporary file
        with open(temp_file.name, 'wb') as f:
            f.write(response.content)
        # Return the temporary file path
        return temp_file.name
    else:
        print(f"Error generating speech: {response.status_code} - {response.text}")
        return None