import discord
from discord.ext import commands, tasks
import os
import rem
import asyncio
import datetime
from dotenv import load_dotenv

load_dotenv()

DISC_BOT = os.getenv("DISC_BOT")

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
        
        # Get the response from gemini.py (your custom response function)
        response_text = rem.gemini_response(user_input)
        
        # Save logs
        export_history_to_csv(user_input, response_text)
        
        # Send the generated response back to the same channel
        await message.channel.send(response_text)

        # Wait for the audio file to appear in Downloads folder and play it
        await asyncio.sleep(1)  # Ensure a short delay to allow time for the file to show up
        
# Start the bot
bot.run(DISC_BOT)
