import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from multiprocessing import Process, Queue
from localtts import start_localtts_process  # Import the process handling function
import datetime

load_dotenv()

DISC_BOT = os.getenv("DISC_BOT")

# Set up the bot
intents = discord.Intents.default()
intents.message_content = True  # Make sure to enable this intent in your Discord Developer Portal

bot = commands.Bot(command_prefix='!', intents=intents)

# Function to export chat history to CSV
def export_history_to_csv(user_input, response, filename="chat_history.csv"):
    """Append user input and response to the chat history CSV file."""    
    # Get the current timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Create a dictionary for the new log entry
    log_entry = {
        "Timestamp": timestamp,
        "User": user_input.strip(),  # Strip extra spaces/newlines
        "Rem": response.strip()   # Strip extra spaces/newlines
    }
    
    # Check if the file exists using os.path.exists()
    file_exists = os.path.exists(filename)
    
    # Open the file and append the new log entry
    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        # Write the header only if the file is new
        if not file_exists:
            file.write('"Timestamp", "User", "Rem"\n')
        # Format the log entry with spaces after the commas
        formatted_entry = f'"{log_entry["Timestamp"]}", "{log_entry["User"]}", "{log_entry["Rem"]}"\n'
        file.write(formatted_entry)
        file.flush()

# Event when the bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

# Listen for messages in a specific channel
@bot.event
async def on_message(message):
    # Make sure the bot doesn't respond to its own messages
    if message.author == bot.user:
        return
    
    # Specify the channel ID you want to listen to (replace with your channel ID)
    target_channel_id = 1248111106480803840  # Replace with your channel ID
    if message.channel.id == target_channel_id:
        user_input = message.content
        
        # Check if the user input is empty
        if not user_input.strip():
            await message.channel.send("Please provide some text!")
            return
        
        # Get the response from gemini.py (your custom response function)
        response_text = "This is a test response"  # Example, replace with actual function
        
        # Save logs (same as before)
        export_history_to_csv(user_input, response_text)
        
        # Send the generated response back to the same channel
        await message.channel.send(response_text)

        # Send the response text to the queue for processing in localtts.py
        queue.put(response_text)
        
        # Wait for the audio file to be returned
        recent_wav_file = queue.get()
        
        if recent_wav_file:
            # Check if the bot is already in a voice channel
            voice_channel = discord.utils.get(bot.voice_clients, guild=message.guild)
            
            if voice_channel is None:
                # The bot is not connected to a voice channel, so join the user's channel
                if message.author.voice:
                    channel = message.author.voice.channel  # Get the voice channel the user is in
                    voice_channel = await channel.connect()  # Join the voice channel
                else:
                    await message.channel.send("You need to join a voice channel first!")
                    return

            # Play the audio file
            voice_channel.play(discord.FFmpegPCMAudio(recent_wav_file), after=lambda e: print('done', e))

            # Optionally, disconnect after playing the audio
            while voice_channel.is_playing():
                await discord.utils.sleep_until(voice_channel.is_playing())  # Wait for audio to finish

            await voice_channel.disconnect()  # Disconnect after audio is done

# Start the bot and the localtts process
if __name__ == "__main__":
    queue = Queue()
    process = Process(target=start_localtts_process, args=(queue,))
    process.start()
    
    # Start the bot
    bot.run(DISC_BOT)  # Replace with your bot's token
    
    # Ensure the localtts process is stopped when the bot stops
    process.terminate()