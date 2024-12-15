import os
import glob
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from multiprocessing import Queue

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

# Initialize the WebDriver (open the browser only once)
driver = webdriver.Chrome()

# Navigate to the webpage (only needs to be done once)
driver.get("http://localhost:9872/")

# Function to handle text input and audio download
def generate_audio_from_text(input_text, queue):
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

    # Wait until the file is downloaded (check every 1 second)
    recent_wav_file = None
    while recent_wav_file is None:
        recent_wav_file = get_most_recent_wav(downloads_folder)
        time.sleep(1)  # Wait for 1 second before checking again

    # Put the file path into the queue to be returned
    queue.put(recent_wav_file)

# To start the WebDriver process
def start_localtts_process(queue):
    print("WebDriver running and waiting for inputs...")
    while True:
        input_text = queue.get()  # Get the input text from the queue
        if input_text == 'exit':
            break  # Terminate the process if 'exit' is received
        generate_audio_from_text(input_text, queue)
