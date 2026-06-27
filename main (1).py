from yt_function import *  # Import all your functions

def main():
    open_youtube()  # Open YouTube in a browser
    while True:  # Infinite loop to listen for commands
        command = recognize_voice_commands()  # Listen for voice commands
        if command:  # If a command is recognized
            print(f"Recognized command: {command}")  # Debugging log

            # Normalize the recognized command (convert to lowercase and strip whitespace)
            normalized_command = command.strip().lower()
            words = normalized_command.split()  # Split the normalized command into words

            # Define your voice commands dictionary (all commands lowercase and trimmed)
            voice_commands = {
                "close youtube": close_youtube,
                "closed" : close_youtube,
                "full": fullscreen,
                "full screen": fullscreen,
                "start": play_video,
                "stop": pause_video,
                "stopped": pause_video,
                "pause": pause_video,
                "mute": mute_unmute_video,
                "unmute": mute_unmute_video,
                "speedup": speed_up,
                "speed up": speed_up,
                "speeddown": speed_down,
                "speed down": speed_down,
                "caption": captions,
                "captions": captions,
                "theater": theater_mode,
                "theatre mode" : theater_mode,
                "theatre": theater_mode,
                "scroll up": scroll_up,
                "up" : scroll_up,
                "down": scroll_down,
                "scroll down": scroll_down,
                "next video": play_next_video,  # Match 'next video'
                "next": play_next_video,  # Match 'next'
                "like": like,
                "liked": like,
                "unlike": like,
                "dislike": dislike,
                "disklked": dislike,
                "autoplay": auto_play,
                "auto": auto_play,
                "subscribe": subscribe,
                "unsubscribe": unsubscribe,
                "mini": mini_mode,
                "expand": expand,
                "home": go_to_home,
                "search": search,
                "voice search": search,
                "first": lambda: play_video_by_position(1),
                "second": lambda: play_video_by_position(2),
                "third": lambda: play_video_by_position(3),
                "back": go_back,
                "volumeup": increase_volume,
                "volume up": increase_volume,
                "volumedown": decrease_volume,
                "volume down": decrease_volume
            }

            # Step 1: Try exact matching for "volume up" and "volume down" first
            if "volume up" in normalized_command:
                print("Exact match for 'volume up'.")
                increase_volume()  # Increase volume
                continue  # Move to the next iteration of the loop

            elif "volume down" in normalized_command:
                print("Exact match for 'volume down'.")
                decrease_volume()  # Decrease volume
                continue  # Move to the next iteration of the loop

            # Step 2: Try other exact matches
            if normalized_command in voice_commands:
                print(f"Exact match found for command: {normalized_command}")
                voice_commands[normalized_command]()  # Call the corresponding function
                if normalized_command == "close youtube":
                    print("YouTube closed. Exiting the program.")
                    break  # Exit after closing YouTube

            # Step 3: If no exact match, check for partial matches for next video
            elif "next video" in normalized_command or "next" in normalized_command:
                print(f"Partial match for 'next video' or 'next': {normalized_command}")
                play_next_video()  # Manually call play_next_video for 'next' or 'next video'

            # Step 4: Check for partial matches based on individual words
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
