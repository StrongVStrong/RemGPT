import discord
from discord.ext import commands, tasks
import os
import rem
import asyncio
import datetime
from dotenv import load_dotenv
import requests

load_dotenv()

DISC_BOT = os.getenv("DISC_BOT")

#My ID
OWNER_ID = os.getenv("OWNER_ID")

API_KEY = os.getenv("key")

API_URL = "https://api.sambanova.ai/v1/chat/completions"

# Set up the bot
intents = discord.Intents.default()
intents.message_content = True  # Make sure to enable this intent in your Discord Developer Portal

bot = commands.Bot(command_prefix='!', intents=intents)

# Folder to monitor
downloads_folder = os.path.expanduser('~/Downloads')

# Track the most recent audio file
last_audio_file = None

# Function to export chat history to CSV
def export_history_to_csv(user_input, response, filename="chat_history.csv"):
    """Append user input and response to the chat history CSV file."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = {
        "Timestamp": timestamp,
        "User": user_input.strip(),
        "Rem": response.strip()
    }
    
    file_exists = os.path.exists(filename)
    
    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        if not file_exists:
            file.write('"Timestamp", "User", "Rem"\n')
        formatted_entry = f'"{log_entry["Timestamp"]}", "{log_entry["User"]}", "{log_entry["Rem"]}"\n'
        file.write(formatted_entry)
        file.flush()
        
    # Now, for appending Rem's entry to a separate text file
    rem_filename = 'rem_responses.txt'  # You can change this to your desired file name

    with open(rem_filename, mode='a', encoding='utf-8') as rem_file:
        rem_file.write(f'"{log_entry["User"]}", "{log_entry["Rem"]}\n')
        rem_file.flush()

# Function to check the Downloads folder for the most recent audio file
async def check_for_audio_file():
    global last_audio_file
    while True:
        # Get the list of files in the downloads folder
        files = [f for f in os.listdir(downloads_folder) if f.endswith('.wav')]
        
        if files:
            # Get the most recent file by modification time
            most_recent_file = max(files, key=lambda f: os.path.getmtime(os.path.join(downloads_folder, f)))
            
            if most_recent_file != last_audio_file:
                last_audio_file = most_recent_file
                print(f"Found new audio file: {most_recent_file}")
                
                # Play the audio file if it's new
                await play_audio_file(most_recent_file)
        
        # Wait a second before checking again
        await asyncio.sleep(1)

# Function to play the audio file in the user's voice channel
async def play_audio_file(audio_file):
    voice_channel = discord.utils.get(bot.voice_clients, guild=bot.get_guild(1235990433457508383))  # Replace with your guild ID

    # If not already in a voice channel, check for the user and join if needed
    if voice_channel is None:
        voice_channel = await join_voice_channel()

    if voice_channel:
        audio_path = os.path.join(downloads_folder, audio_file)
        voice_channel.play(discord.FFmpegPCMAudio(audio_path), after=lambda e: print(f"Finished playing {audio_file}"))
        
        while voice_channel.is_playing():
            await asyncio.sleep(1)  # Wait until the audio finishes before continuing

# Function to join the user's voice channel
async def join_voice_channel():
    for member in bot.get_all_members():
        if member.voice:
            channel = member.voice.channel
            voice_channel = await channel.connect()
            print(f"Joined {channel.name}!")
            return voice_channel
    print("No user in a voice channel to join.")
    return None

# Event when the bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    # Start checking for audio files in the background
    bot.loop.create_task(check_for_audio_file())

# Read multiple text files and concatenate their content
files = ['remmie.txt', 'rem_responses.txt']
combined_prompt = ""
chat_memory = []
for file in files:
    if file == 'rem_responses.txt':
        # Read only the last 16 lines from rem_responses.txt
        with open(file, 'r', encoding='utf-8') as f:
            lines = f.readlines()[-16:]  # Get the last 16 lines
            combined_prompt += "".join(lines) + "\n\n"
    else:
        # Read the entire content for other files
        with open(file, 'r', encoding='utf-8') as f:
            combined_prompt += f.read() + "\n\n"

# Function to get AI response
def get_ai_response(user_input, user_id):
    """Fetches a response from the AI API with owner-specific handling."""
    global chat_memory
    # Check if the user is the owner
    if str(user_id) == str(OWNER_ID):
        # Special handling for the owner's message
        prompt = f"(This MSG IS From Belan, with User ID: {OWNER_ID}): {user_input}"
    else:
        # General handling for other users
        prompt = f"(This MSG is NOT from Belan, they are User ID: {user_id}): {user_input}"
    chat_memory.append({"role": "user", "content": prompt})
    messages = [{"role": "system", "content": combined_prompt}] + chat_memory
    # Prepare the API payload
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "Meta-Llama-3.1-70B-Instruct",
        "messages": messages,
        "temperature": 0.8,
        "top_p": 0.1,
        "max_tokens": 200
    }

    try:
        # Send the request to the API
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()  # Raise an error for non-200 responses
        
        # Extract the AI's response
        ai_response = response.json()['choices'][0]['message']['content']
        
        # Append the AI's response to the memory
        chat_memory.append({"role": "assistant", "content": ai_response})
        
        return ai_response
    except Exception as e:
        return f"Error fetching response: {str(e)}"


# Listen for messages in a specific channel
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    target_channel_id = 1248111106480803840  # Replace with your channel ID
    if message.channel.id == target_channel_id:
        user_input = message.content
        
        # Check if the user input is empty
        if not user_input.strip():
            await message.channel.send("Please provide some text!")
            return
        
        # Get the response from gemini.py
        response_text = get_ai_response(user_input, message.author.id)
        
        # Save logs
        export_history_to_csv(user_input, response_text)
        
        # Send the generated response back to the same channel
        await message.channel.send(response_text)

        # Wait for the audio file to appear in Downloads folder and play it
        await asyncio.sleep(1)
        
# Start the bot
bot.run(DISC_BOT)
