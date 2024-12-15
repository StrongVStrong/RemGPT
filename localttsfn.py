from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pydub import AudioSegment
from pydub.playback import play
import os
import glob
import time

# Initialize the WebDriver
driver = webdriver.Chrome()

# Navigate to the webpage
driver.get("http://localhost:9872/")

# Path to the Downloads folder
downloads_folder = r"C:\Users\Megas\Downloads"

# Function to get the most recently downloaded .wav file
def get_most_recent_wav(download_folder):
    # Get a list of all .wav files in the Downloads folder
    wav_files = glob.glob(os.path.join(download_folder, "*.wav"))

    # If there are no .wav files, return None
    if not wav_files:
        return None

    # Get the most recently modified file
    most_recent_file = max(wav_files, key=os.path.getmtime)

    return most_recent_file

# Function to handle the text input and audio download
def process_input(input_text):
    # Wait for the textarea input box to be available
    input_box = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="component-25"]/label/textarea'))
    )

    # Enter text into the input box
    input_box.clear()  # Clear previous text if any
    input_box.send_keys(input_text)

    # Wait for the submit button to become clickable and then click it
    submit_button = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="component-41"]'))
    )
    submit_button.click()

    # Wait for the download button to appear
    download_button = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="component-42"]/div[2]/a/button'))
    )

    # Click the download button
    download_button.click()

# Loop to continuously input text and download audio
last_played_file = None  # Track the last played file to avoid playing the same one

while True:
    # Ask for new text input (you can change this to any other way to get text input)
    user_input = input("Enter text to convert to speech (or type 'exit' to stop): ")

    if user_input.lower() == 'exit':
        print("Exiting the loop.")
        break  # Exit the loop if the user types 'exit'

    # Process the input (enter text, submit, and download)
    process_input(user_input)
    time.sleep(0.2)

    # Wait until a new file is downloaded (check every 1 second)
    recent_wav_file = None
    while recent_wav_file is None:
        recent_wav_file = get_most_recent_wav(downloads_folder)
        time.sleep(1)  # Wait for 1 second before checking again

    # Ensure it's a new file (not the same as the last played one)
    if recent_wav_file != last_played_file:
        print(f"Playing the most recent file: {recent_wav_file}")
        # Load and play the audio
        audio = AudioSegment.from_file(recent_wav_file)
        play(audio)

        # Update the last played file
        last_played_file = recent_wav_file
    else:
        print("The same file was downloaded again, waiting for a new one.")
        # You can choose to wait longer or take other actions here

# Function to get the most recent audio file without playing it
def get_most_recent_audio_file():
    recent_wav_file = get_most_recent_wav(downloads_folder)
    return recent_wav_file

# Example usage of the function to get the most recent audio file:
recent_file = get_most_recent_audio_file()
if recent_file:
    print(f"Most recent audio file: {recent_file}")
else:
    print("No .wav files found in the Downloads folder.")

# Close the browser after the loop ends
driver.quit()
