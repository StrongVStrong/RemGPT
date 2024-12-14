# play.py
import rem
import remtts
import datetime
import os

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

def main():
    while True:
        user_input = input("You: ")
        
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye! Come back soon.")
            break
        
        # Get response from gemini.py
        response_text = rem.gemini_response(user_input)
        
        # Save logs
        export_history_to_csv(user_input, response_text)

        # Print Vegito's response
        print(f"Rem: {response_text}")
        
        # Call play.py to generate and play the speech
        remtts.gen_audio(response_text)
        

if __name__ == "__main__":
    main()
