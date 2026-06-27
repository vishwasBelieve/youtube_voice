from shorts_function import *  # Import all your functions

def main():
    play_shorts()  # Open YouTube in a browser
    while True:  # Infinite loop to listen for commands
        command = recognize_voice_commands()  # Listen for voice commands
        if command:  # If a command is recognized
            print(f"Recognized command: {command}")  # Debugging log

            # Normalize the recognized command (convert to lowercase and strip whitespace)
            normalized_command = command.strip().lower()
            words = normalized_command.split()  # Split the normalized command into words

            # Define your voice commands dictionary (all commands lowercase and trimmed)
            voice_commands = {
                "close youtube": close_youtubeS,
                "start": play_video,
                "stop": pause_video,
                "pause": pause_video,
                "mute": mute_unmute,
                "unmute": mute_unmute,
                "scroll up": scroll_up,
                "up" : scroll_up,
                "down": scroll_down,
                "scroll down": scroll_down,
                "like": like,
                "liked": like,
                "unlike": like,
                "dislike": dislike,
                "disklked": dislike,
                "open": open_comments,
                "opned":open_comments,
                "open comments": open_comments,
                "opencomments": open_comments,
                "closed comments": close_comments,
                "close comments": close_comments,
                "next": next_short,
                "next short" : next_short,
                "previous short": previous_short,
                "previous" : previous_short,
                "volumeup": increase_volume,
                "volume up": increase_volume,
                "volumedown": decrease_volume,
                "volume down": decrease_volume

            }

            # First try exact matching for the whole command
            if normalized_command in voice_commands:
                print(f"Exact match found for command: {normalized_command}")
                voice_commands[normalized_command]()  # Call the corresponding function
                if normalized_command == "close youtube":
                    print("YouTube closed. Exiting the program.")
                    break  # Exit after closing YouTube

            # If no exact match, check for more specific partial matches first
            elif "next video" in normalized_command or "next" in normalized_command:
                print(f"Partial match for 'next video' or 'next': {normalized_command}")
                next_short()  # Manually call play_next_video for 'next' or 'next video'

            # Check for partial matches based on individual words
            elif any(word in voice_commands for word in words):
                for word in words:
                    if word in voice_commands:
                        print(f"Partial match found for word: {word}")
                        voice_commands[word]()  # Execute the corresponding command
                        break

            else:
                print(f"No matching command found for: {command}")

if __name__ == "__main__":
    main()
