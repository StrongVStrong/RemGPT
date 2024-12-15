import os
import glob
import time
import pyautogui
import discord
from discord.ext import commands
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from queue import Queue
from dotenv import load_dotenv
import asyncio

load_dotenv()

# Discord Bot Token
DISC_BOT = os.getenv("DISC_BOT")

# Path to the Downloads folder
downloads_folder = r"C:\Users\Megas\Downloads"

# List of file paths to select
files_to_select = [
    r'"C:\Users\Megas\Documents\Samples\hutao1.wav"',  # Replace with your actual file paths
    r'"C:\Users\Megas\Documents\Samples\hutao2.wav"',
    r'"C:\Users\Megas\Documents\Samples\hutao3.wav"',
    r'"C:\Users\Megas\Documents\Samples\hutao4.wav"'
]

# Initialize the WebDriver (open the browser only once)
driver = webdriver.Chrome()

# Initialize the queue for managing incoming messages
queue = Queue()

# Function to get the most recent .wav file from the Downloads folder
def get_most_recent_wav(download_folder):
    wav_files = glob.glob(os.path.join(download_folder, "*.wav"))
    if not wav_files:
        return None
    return max(wav_files, key=os.path.getmtime)

# Set up the bot
intents = discord.Intents.default()
intents.message_content = True  # Make sure to enable this intent in your Discord Developer Portal
bot = commands.Bot(command_prefix='!', intents=intents)

# Function to process text input and download the audio file
def process_input(input_text):
    # Open the page only once
    driver.get("http://localhost:9872/")

    # Wait for the button to open file explorer and click it
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="component-11"]/div[2]/button'))
    ).click()

    time.sleep(1)  # Give time for file explorer to appear

    # Use pyautogui to type the Downloads folder path into the file explorer dialog
    pyautogui.typewrite(downloads_folder)
    pyautogui.press('enter')

    time.sleep(1)  # Wait for file dialog to appear

    # Select the files
    file_paths_to_select = ' '.join(files_to_select)
    pyautogui.typewrite(file_paths_to_select)  # Type all file paths with space separation
    pyautogui.press('enter')

    # Wait for the text area and enter text
    input_box = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="component-15"]/label/textarea'))
    )
    input_box.clear()
    input_box.send_keys(input_text)

    # Submit the text
    submit_button = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="component-20"]/button'))
    )
    submit_button.click()

    # Wait for the download button to appear and click it
    download_button = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="component-42"]/div[2]/a/button'))
    )
    download_button.click()

    # Wait for the file to download
    recent_wav_file = None
    while recent_wav_file is None:
        recent_wav_file = get_most_recent_wav(downloads_folder)
        time.sleep(1)

    return recent_wav_file

# Define the queue for storing messages
queue = Queue()

# Set up the bot
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True  # Ensure the bot can track voice states (for user voice channel info)
bot = commands.Bot(command_prefix='!', intents=intents)

# Function to join the first available voice channel with members
async def join_first_available_vc(guild):
    for voice_channel in guild.voice_channels:
        if len(voice_channel.members) > 0:  # Check if there are members in the channel
            return voice_channel
    return None  # Return None if no voice channels have members

# Function to play audio in the voice channel
async def play_audio_in_vc(voice_channel, audio_file_path):
    # Make sure the bot is connected to the voice channel
    if not voice_channel.guild.voice_client:
        await voice_channel.connect()

    # Play the audio file in the voice channel
    voice_channel.play(discord.FFmpegPCMAudio(audio_file_path), after=lambda e: print('done', e))
    
    # Wait for the audio to finish playing
    while voice_channel.is_playing():
        await discord.utils.sleep_until(voice_channel.is_playing())
        
# Function to process the queue and play audio messages
async def process_queue():
    while True:
        if not queue.empty():
            input_text = queue.get()  # Get the input text from the queue
            recent_wav_file = process_input(input_text)  # Process the input text to generate audio

            # You can now use the `recent_wav_file` to send it to a voice channel or elsewhere
            print(f"Generated audio file: {recent_wav_file}")

            # Get the first available voice channel with members
            guild = bot.get_guild(GUILD_ID)  # Replace with your guild ID
            voice_channel = await join_first_available_vc(guild)

            if voice_channel:
                await play_audio_in_vc(voice_channel, recent_wav_file)
            else:
                print("No voice channels with members available")

# Event when the bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

# Listen for messages in a specific channel
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Specify the channel ID you want to listen to (replace with your channel ID)
    target_channel_id = 123456789012345678  # Replace with your channel ID
    specific_user_id = 987654321098765432  # Replace with the user ID you want to listen to

    # Only process messages from the specified user or bot in the target channel
    if message.channel.id == target_channel_id and message.author.id == specific_user_id:
        user_input = message.content
        
        # Check if the user input is empty
        if not user_input.strip():
            return  # Do nothing if the input is empty

        # Put the user input into the queue for processing (you can call the function to handle TTS)
        queue.put(user_input)

    else:
        # Ignore messages from other users/bots
        pass
# Start the bot and process the queue
async def start_bot_and_process():
    await bot.start(DISC_BOT)  # Replace with your bot's token
    await process_queue()  # Start processing the queue

# Start the bot loop
asyncio.run(start_bot_and_process())