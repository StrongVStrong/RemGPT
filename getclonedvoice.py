import requests
import os
import pygame
from dotenv import load_dotenv

load_dotenv()
# Initialize pygame mixer for audio playback
pygame.mixer.init()

api_key = os.getenv("Papi_key") #Enter your PlayHT API key here/your .env file
user_id = os.getenv("user_id") #Enter your PlayHT user ID here/your .env file

# Check that the User ID is correctly set
print(f"Using User ID: {user_id}")  # Debugging output

# PlayHT API URL for cloned voices
url = "https://api.play.ht/api/v2/cloned-voices"

# Headers with authentication information
headers = {
    "Authorization": f"Bearer {api_key}",
    "X-User-Id": user_id  # Ensure this is a string with exactly 28 characters
}

# Print headers for debugging
print("Headers being sent:", headers)

# Send GET request to fetch cloned voices
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    cloned_voices = response.json()  # Parse the JSON response
    print("Cloned Voices:", cloned_voices)
else:
    print(f"Error fetching cloned voices: {response.status_code} - {response.text}")
