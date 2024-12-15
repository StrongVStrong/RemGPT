import time
import multiprocessing
from ttstest import start_localtts_process  # Import the function from your main program

# Queue to send text input to TTS generator
queue = multiprocessing.Queue()

# Start the TTS generator process
process = multiprocessing.Process(target=start_localtts_process, args=(queue,))
process.start()

# Function to send text to TTS program
def send_to_tts(text):
    print(f"Sending text to TTS: {text}")
    queue.put(text)  # Send the text to the TTS queue

# Main loop to send text to the TTS program
while True:
    user_input = input("Enter text to convert to speech (or type 'exit' to stop): ")
    
    if user_input.lower() == 'exit':
        print("Exiting the loop.")
        queue.put('exit')  # Sending exit signal to the TTS process
        break  # Terminate the process
    else:
        send_to_tts(user_input)  # Send the text for TTS conversion
        time.sleep(1)  # Wait for a short time before next input (adjust as necessary)

# Terminate the process after the loop ends
process.join()
