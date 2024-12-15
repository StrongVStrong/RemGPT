import os
import glob
import time
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.by import By
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

# List of file paths to select
files_to_select = [
    r'"C:\Users\Megas\Documents\Samples\hutao1.wav"',  # Replace with your actual file paths
    r'"C:\Users\Megas\Documents\Samples\hutao2.wav"',  
    r'"C:\Users\Megas\Documents\Samples\hutao3.wav"',  
    r'"C:\Users\Megas\Documents\Samples\hutao4.wav"'
]

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

# Wait for the file selector to open, and now select all the specified files
time.sleep(1)  # Wait for the file selector to open

# Use pyautogui to select all the files at once in the file dialog
# Join the file paths with spaces as Windows uses spaces for multiple selections
file_paths_to_select = ' '.join(files_to_select)

# Type the full file paths and press Enter to select all the files
pyautogui.typewrite(file_paths_to_select)  # Type all file paths with space separation
pyautogui.press('enter')  # Press Enter to confirm the selection

# Wait for the first listbox to be available and select "English"
listbox1 = WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="component-19"]/div[2]/div/div[1]/div/input'))
)

# Click to open the listbox and delete any existing text
listbox1.click()
time.sleep(0.5)  # Allow dropdown to appear
pyautogui.hotkey('ctrl', 'a')  # Select all text
pyautogui.press('backspace')  # Delete all text
pyautogui.typewrite("English")  # Type "English"
pyautogui.press('enter')  # Press Enter to confirm the selection

# Wait for the second listbox to be available and select the "English" option
listbox2 = WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="component-28"]/div[2]/div/div[1]/div/input'))
)

# Click to open the second listbox and delete any existing text
listbox2.click()
time.sleep(0.5)  # Allow dropdown to appear
pyautogui.hotkey('ctrl', 'a')  # Select all text
pyautogui.press('backspace')  # Delete all text
pyautogui.typewrite("English")  # Type "English"
pyautogui.press('enter')  # Press Enter to confirm the selection

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