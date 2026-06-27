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
        audio = recognizer.listen(source)

    try:
        # Predefined list of commands
        commands =['close youtube', 'full', 'liked','disliked','full screen', 'start', 'stop', 'pause', 'mute', 'unmute', 
        'speedup', 'speed up', 'speeddown', 'speed down', 'caption','captions', 'theater', 'theatre mode', 'theatre',
         'scroll up', 'up', 'down', 'scroll down', 'next video',
         'next', 'like', 'unlike', 'dislike', 'autoplay', 'auto', 'subscribe', 'unsubscribe', 'mini', 'expand',
         'home', 'search', 'voice search', 'first', 'second', 'third', 'back']
        
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





# Function to open YouTube using Selenium
def open_youtube():
    global driver  # Use the global driver variable
    if driver is None:  # Only open a new instance if it's not already opened
        print("Driver is None. Calling create_driver()...")
        driver = create_driver()  # <-- Store the returned driver in the global variable
        if driver is None:
            print("Failed to initialize driver.")
        else:
            driver.get("https://www.youtube.com")  # Open YouTube
            print("YouTube opened in Chrome.")
    else:
        print("YouTube is already open.")


def close_youtube():
    global driver  # Use the global driver variable
    if driver is not None:  # Only close if the driver is initialized
        driver.quit()  # Close the driver
        driver = None  # Reset driver to None
        print("YouTube closed. Exiting the program.")
        return True  # Return True to signal that the program should exit
    else:
        print("YouTube is not open.")
    return False


def fullscreen():
    global driver
    if driver is not None:
        try:
            time.sleep(0.2)
            pyautogui.press('f')
            print("Video is now in fullscreen mode.")
        except Exception as e:
            print(f"Error in going fullscreen: {e}")
    else:
        print("YouTube is not open.")


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

def mute_unmute_video():
    global driver
    if driver:
        try:
            driver.execute_script("document.querySelector('#movie_player > div.ytp-chrome-bottom > div.ytp-chrome-controls > div.ytp-left-controls > span > button').click()")
            print("YouTube video muted.")
        except Exception as e:
            print(f"Error muting video: {e}")

# Speed up the video
def speed_up():
    global driver
    if driver:
        try:
            driver.execute_script("""
                var videoElement = document.querySelector('video');
                if (videoElement) {
                    videoElement.playbackRate += 0.25;  // Increase speed by 0.25x
                    console.log('Speed increased to: ' + videoElement.playbackRate);
                } else {
                    console.log('No video element found.');
                }
            """)
            print("Speeding up the video.")
        except Exception as e:
            print(f"Error in speeding up video: {e}")

# Slow down the video
def speed_down():
    global driver
    if driver:
        try:
            driver.execute_script("""
                var videoElement = document.querySelector('video');
                if (videoElement) {
                    videoElement.playbackRate -= 0.25;  // Decrease speed by 0.25x
                    console.log('Speed decreased to: ' + videoElement.playbackRate);
                } else {
                    console.log('No video element found.');
                }
            """)
            print("Slowing down the video.")
        except Exception as e:
            print(f"Error in slowing down video: {e}")


def captions():
    global driver
    if driver:
        try:
            # Execute JavaScript to click the captions (CC) button
            driver.execute_script("document.querySelector('.ytp-subtitles-button').click();")
            print("Toggled captions.")
        except Exception as e:
            print(f"Error toggling captions: {e}")
    else:
        print("YouTube is not open.")

def theater_mode():
    global driver
    if driver:
        try:
            driver.execute_script("document.querySelector('#movie_player > div.ytp-chrome-bottom > div.ytp-chrome-controls > div.ytp-right-controls > button.ytp-size-button.ytp-button').click();")
            print("now in theater mode")
        except Exception as e:
            print(f"Error in theater mode: {e}")
def mini_mode():
    global driver
    if driver:
        try:
            driver.execute_script("document.querySelector('#movie_player > div.ytp-chrome-bottom > div.ytp-chrome-controls > div.ytp-right-controls > button.ytp-miniplayer-button.ytp-button').click();")
            print("now playing in miniplayer")
        except Exception as e:
            print(f"Error in miniplayer: {e}")

def expand():
    global driver
    if driver:
        try:
            driver.execute_script("document.querySelector('#movie_player > div.ytp-miniplayer-ui > div > button.ytp-miniplayer-expand-watch-page-button.ytp-button.ytp-miniplayer-button-top-left').click();")
            print("now playing in explan mode")
        except Exception as e:
            print(f"Error in expaning video: {e}")

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



def play_next_video():
    global driver
    if driver is not None:
        try:
            driver.execute_script("document.querySelector('#movie_player > div.ytp-chrome-bottom > div.ytp-chrome-controls > div.ytp-left-controls > a.ytp-next-button.ytp-button').click();")
            print("Playing the next video.")
        except Exception as e:
            print(f"Error playing the next video: {e}")
    else:
        print("YouTube is not open.")

def auto_play():
    global driver
    if driver is not None:
        try:
            driver.execute_script("document.querySelector('#movie_player > div.ytp-chrome-bottom > div.ytp-chrome-controls > div.ytp-right-controls > button:nth-child(2)').click();")
            print("autoplay is on")
        except Exception as e:
            print(f"Error in autoplaying: {e}")
    else:
        print("YouTube is not open.")

def like():
    global driver
    if driver is not None:
        try:
            driver.execute_script("document.querySelector('#top-level-buttons-computed > segmented-like-dislike-button-view-model > yt-smartimation > div > div > like-button-view-model > toggle-button-view-model > button-view-model > button').click();")
            print("liked the video")
        except Exception as e:
            print(f"Error in liking the video: {e}")
    else:
        print("YouTube is not open.")

def dislike():
    global driver
    if driver is not None:
        try:
            driver.execute_script("document.querySelector('#top-level-buttons-computed > segmented-like-dislike-button-view-model > yt-smartimation > div > div > dislike-button-view-model > toggle-button-view-model > button-view-model > button').click();")
            print("disliked the video")
        except Exception as e:
            print(f"Error in disliking the video: {e}")
    else:
        print("YouTube is not open.")

def subscribe():
    global driver
    if driver is not None:
        try:
            driver.execute_script("document.querySelector('#subscribe-button-shape > button').click();")
            print("Subscribed")
        except Exception as e:
            print(f"Error in  subscribing the channel: {e}")
    else:
        print("YouTube is not open.")

def unsubscribe():
    global driver
    if driver is not None:
        try:
            driver.execute_script("document.querySelector('#subscribe-button-shape > button').click();")
            time.sleep(0.5)
            driver.execute_script("document.querySelector('#confirm-button > yt-button-shape > button').click();")
            print("Unsbscribed")
        except Exception as e:
            print(f"Error in  unsubscribing the channel: {e}")
    else:
        print("YouTube is not open.")

def search():
    global driver 
    if driver is not None:
        try:
         driver.execute_script("document.querySelector('#voice-search-button > ytd-button-renderer > yt-button-shape > button').click();")
         print("searching through voice")
        except Exception as e:
            print(f"Error in voice searching: {e}");

def go_to_home():
    global driver
    if driver is not None:
        try:
            # Find and click the Home button using JavaScript
            driver.execute_script("""
                var homeButton = document.querySelector('a[title="Home"]') || document.querySelector('a[href="/"]');
                if (homeButton) {
                    homeButton.click();
                    console.log("Navigated to Home.");
                } else {
                    console.log("Home button not found.");
                }
            """)
            print("Navigated to YouTube Home.")
        except Exception as e:
            print(f"Error navigating to Home: {e}")
    else:
        print("YouTube is not open.")


def play_video_by_position(position):
    global driver
    try:
        videos = driver.find_elements("xpath", '//a[@id="video-title"]')
        if len(videos) >= position:
            videos[position - 1].click()  # Click the nth video (1-based index)
            print(f"Playing video {position}.")
        else:
            print(f"Only {len(videos)} videos found, but you requested the {position}th video.")
    except Exception as e:
        print(f"Error playing video: {e}")

def go_back():
    driver.back()
