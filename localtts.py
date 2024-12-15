import os
import glob
import time
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Path to the Downloads folder
downloads_folder = r"C:\Users\Megas\Downloads"

# Function to get the most recently downloaded .wav file
def get_most_recent_wav(download_folder):
    wav_files = glob.glob(os.path.join(download_folder, "*.wav"))
    if not wav_files:
        return None
    return max(wav_files, key=os.path.getmtime)

# Initialize the WebDriver (open the browser only once)
driver = webdriver.Chrome()

# Navigate to the webpage (only needs to be done once)
driver.get("http://localhost:9872/")

# Wait for the button to open file explorer and click it
WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="component-11"]/div[2]/button'))
).click()

# After the file explorer is triggered, wait for it to appear and type the path to Downloads folder
time.sleep(1)  # Give time for file explorer to appear

# Use pyautogui to type the Downloads folder path into the file explorer dialog
print(f"Typing file path: {downloads_folder}")
pyautogui.typewrite(downloads_folder)  # Type the path to the folder
pyautogui.press('enter')  # Press Enter to confirm

# Wait for the textarea to appear and enter the text "hello this is the sample text"
input_box = WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="component-15"]/label/textarea'))
)
input_box.clear()  # Clear any previous input
input_box.send_keys("Hello this is the sample text")  # Enter the sample text

# Click the submit button to process the input
submit_button = WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="component-20"]/button'))
)
submit_button.click()

# List of specific file paths to select from the Downloads folder
files_to_select = [
    os.path.join(downloads_folder, "test"),
    os.path.join(downloads_folder, "test1"),
    os.path.join(downloads_folder, "test2"),
    os.path.join(downloads_folder, "test3")
]

# Select each file from the file dialog
for file in files_to_select:
    # Assuming the file input is accessible by its value attribute
    # Adjust the XPath if necessary, depending on the page structure
    file_input = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, f"//input[@value='{file}']"))
    )
    file_input.click()  # Select each file

# After file selection, proceed with entering the final text
final_input_box = WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="component-25"]/label/textarea'))
)
final_input_box.clear()
final_input_box.send_keys("Hello this is the final input text")  # Enter the final text

# Click the submit button to proceed
final_submit_button = WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="component-41"]'))
)
final_submit_button.click()

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

# Print the path of the downloaded audio file
print(f"Generated audio file path: {recent_wav_file}")

# Quit the WebDriver after everything is done
driver.quit()
