
from plyer import notification
from playsound import playsound
import os

def show_notification(title, message):
    print("DEBUG: Attempting to show notification...")
    try:
        notification.notify(
            title=title,
            message=message,
            app_name='Calendar Reminder',
            timeout=10
        )
        print("DEBUG: notification.notify() called successfully.")
    except Exception as e:
        import traceback
        print(f"ERROR: An exception occurred in show_notification: {e}")
        print("ERROR: Traceback below:")
        traceback.print_exc()

def play_sound():
    try:
        script_dir = os.path.dirname(__file__)
        sound_file = os.path.join(script_dir, 'assets', 'notification.mp3')
        if os.path.exists(sound_file):
            playsound(sound_file)
        else:
            print(f"Sound file not found: {sound_file}")
    except Exception as e:
        print(f"Error playing sound: {e}")
