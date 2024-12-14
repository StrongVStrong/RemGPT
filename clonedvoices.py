import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("Papi_key")  # Enter your PlayHT API key here/your .env file
user_id = os.getenv("user_id")   # Enter your PlayHT user ID here/your .env file

# PlayHT API URL for fetching voices
url = "https://api.play.ht/api/v2/cloned-voices"

# Headers for authentication
headers = {
    "Authorization": f"Bearer {api_key}",
    "X-User-Id": user_id
}

def get_cloned_voices():
    # Send GET request to fetch the voices
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        voices_data = response.json()  # Assuming the response is in JSON format
        
        # If the response is a list
        if isinstance(voices_data, list):
            print("Cloned Voices:")
            for voice in voices_data:
                # Display the voice attributes, adjust these as per your response structure
                print(f"Voice ID: {voice['id']}, Name: {voice['name']}")
        else:
            print("Unexpected response structure. Expected a list.")
    else:
        print(f"Error fetching voices: {response.status_code} - {response.text}")

# Call the function to get and display voices
get_cloned_voices()
