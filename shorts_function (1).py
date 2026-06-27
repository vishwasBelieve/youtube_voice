import speech_recognition as sr
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options 
import pyautogui
import time
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from ctypes import cast, POINTER
import json


# Global variable to keep the driver instance
driver = None


def load_chrome_path():
    # Load the Chrome path from the config.json file
    try:
        with open("config.json", "r") as config_file:
            config = json.load(config_file)
            print("Loaded config:", config)  # Debugging line to print the contents of the JSON
            return config.get("chrome_path", None)  # Return the chrome_path or None if not found
    except Exception as e:
        print(f"Error loading Chrome path from config.json: {str(e)}")
        return None


def create_driver():
    chrome_path = load_chrome_path()

    if not chrome_path:
        print("Chrome path is not set. Please configure the path.")
        return None  # Exit if the path is not found

    chrome_options = Options()  # Initialize Chrome options
    chrome_options.add_argument("--start-maximized")  # Maximize Chrome window
    chrome_options.add_argument(f"--user-data-dir={chrome_path}")  # Use the user data dir (profile)
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Hide automation control
    chrome_options.add_argument("--no-sandbox")  # Required for some environments
    chrome_options.add_argument("--disable-dev-shm-usage")  # Prevent shared memory issues
    chrome_options.add_argument("--disable-infobars")  # Disable info bars
    chrome_options.add_argument("--log-level=3")  # Suppress warning and info logs
    chrome_options.add_argument("--ignore-certificate-errors")  # Ignore SSL errors

    # Specify the path to your ChromeDriver (update this path as needed)
    service = Service('D:\\Project\\chromedriver\\chromedriver.exe')  # Path to your chromedriver
    driver = webdriver.Chrome(service=service, options=chrome_options)  # Create driver with options
    
    return driver  # Return the driver object after initialization


def recognize_voice_commands():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for specific commands...")
        audio = recognizer.listen(source)

    try:
        # Predefined list of commands
        commands = [
    'close youtube', 'start', 'stop', 'pause', 'mute', 
    'unmute', 'caption', 'scroll up', 'up', 'down', 
    'scroll down', 'like', 'liked', 'unlike', 'dislike', 
    'disklked', 'subscribe', 'unsubscribe', 'open', 
    'opned', 'open comments', 'opencomments', 'closed comments', 
    'close comments', 'next', 'next short', 'previous short', 
    'previous'
]
        
        # Convert audio to text using Google's speech recognition service
        command = recognizer.recognize_google(audio).lower()
        
        # Check if the recognized command is in the predefined list
        if any(cmd in command for cmd in commands):
            print(f"Recognized command: {command}")  # Only print once here
            return command
        else:
            print("Sorry, command not recognized.")
            return None

    except sr.UnknownValueError:
        print("Could not understand audio.")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return None

def play_shorts():
    global driver  # Use the global driver variable
    if driver is None:  # Only open a new instance if it's not already opened
        print("Driver is None. Calling create_driver()...")
        driver = create_driver()  # <-- Store the returned driver in the global variable
        if driver is None:
            print("Failed to initialize driver.")
        else:
            driver.get("https://www.youtube.com/shorts")  # Open YouTube
            print("YouTube opened in Chrome.")
    else:
        print("YouTube is already open.")


def close_youtubeS():
    global driver  # Use the global driver variable
    if driver is not None:  # Only close if the driver is initialized
        driver.quit()  # Close the driver
        driver = None  # Reset driver to None
        print("YouTube closed. Exiting the program.")
        return True  # Return True to signal that the program should exit
    else:
        print("YouTube is not open.")
    return False

def pause_video():
    global driver
    if driver is not None:
        try:
            driver.execute_script("""
                    var videoElement = document.querySelector("video");
                    if (videoElement) {
                        videoElement.pause();
                        console.log("Regular video is now paused.");
                    } else {
                        console.log("No video element found in regular video.");
                    }
                """)
            print("video is paused")
        except Exception as e:
            print(f"Error in pausing video: {e}")

def play_video():
    global driver
    if driver is not None:
        try:
            driver.execute_script("""
                    var videoElement = document.querySelector("video");
                    if (videoElement) {
                        videoElement.play();
                        console.log("Regular video is now playing.");
                    } else {
                        console.log("No video element found in regular video.");
                    }
                """)
            print("playing video")

                # play the regular YouTube video
                
        except Exception as e:
            print(f"Error in playing video: {e}")
    else:
        print("YouTube is not open.")

                
# Function to increase the system volume by 25%
def increase_volume():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    
    current_volume = volume.GetMasterVolumeLevelScalar()
    new_volume = min(current_volume + 0.25, 1.0)  # Ensure it doesn't go above 100%
    volume.SetMasterVolumeLevelScalar(new_volume, None)
    print(f"Volume increased to {new_volume * 100:.0f}%")

# Function to decrease the system volume by 25%
def decrease_volume():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    
    current_volume = volume.GetMasterVolumeLevelScalar()
    new_volume = max(current_volume - 0.25, 0.0)  # Ensure it doesn't go below 0%
    volume.SetMasterVolumeLevelScalar(new_volume, None)
    print(f"Volume decreased to {new_volume * 100:.0f}%")




def next_short():
    global driver
    if driver:
        try:
            driver.execute_script("document.querySelector('#navigation-button-down > ytd-button-renderer > yt-button-shape > button').click();")
            print("Next short")
        except Exception as e:
            print(f"Error in playing next short: {e}")


def  previous_short():
    global driver
    if driver:
        try:
            driver.execute_script("document.querySelector('#navigation-button-up > ytd-button-renderer > yt-button-shape > button').click();")
            print("Privous short")
        except Exception as e:
            print(f"Error in playing privous short: {e}")

def like():
    global driver
    if driver:
        try:
            driver.execute_script("document.querySelector('#like-button > yt-button-shape > label > button').click();");
            print("Liked the video.")
        except Exception as e:
            print(f"Error clicking like button: {e}")
    else:
        print("YouTube is not open.")

def dislike():
    global driver
    if driver:
        try:
            driver.execute_script("document.querySelector('#dislike-button > yt-button-shape > label > button').click();");
        except Exception as e:
            print(f"Error clicking like button: {e}")
    else:
        print("YouTube is not open.")

def open_comments():
    global driver
    if driver:
        try:
            driver.execute_script("document.querySelector('#comments-button > ytd-button-renderer > yt-button-shape > label > button').click();")
            time.sleep(1)
            driver.execute_script("document.querySelector('#title').focus();");
            print("Opening comments")
        except Exception as e:
            print(f"Error opening comments: {e}")

def close_comments():
    global driver
    if driver:
        try:
            driver.execute_script("document.querySelector('#visibility-button > ytd-button-renderer > yt-button-shape > button').click();")
            print("Closing comments")
        except Exception as e:
            print(f"Error closing comments: {e}")



def mute_unmute():
    global driver
    if driver is not None:
        try:
            driver.execute_script("document.querySelector('#player-container > div.player-controls.style-scope.ytd-reel-video-renderer > ytd-shorts-player-controls > desktop-shorts-volume-controls > button').click();")
            print("muting/unmuting the video")
        except Exception as e:
            print(f"Error in unsubscribing the channel: {e}")
    else:
        print("YouTube is not open.")

def scroll_up():
    global driver
    if driver:
        try:
            driver.execute_script("window.scrollBy(0, -375);")  # Scroll up by 500 pixels
            print("Scrolling up.")
        except Exception as e:
            print(f"Error in scrolling up: {e}")

def scroll_down():
    global driver
    if driver:
        try:
            driver.execute_script("window.scrollBy(0, 375);")  # Scroll down by 500 pixels
            print("Scrolling down.")
        except Exception as e:
            print(f"Error in scrolling down: {e}")
#creatred by vSMCA0454