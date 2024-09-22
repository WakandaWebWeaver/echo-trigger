import speech_recognition as sr
import os
import platform
import subprocess
import time


def set_volume(volume_level_to_set):
    if platform.system() == 'Darwin':
        script = f"set volume output volume {volume_level_to_set}"
        subprocess.run(["osascript", "-e", script])
    elif platform.system() == 'Windows':
        volume = int(volume_level_to_set * 655.35)
        os.system(f"nircmd.exe setsysvolume {volume}")
    elif platform.system() == 'Linux':
        os.system(f"amixer set Master {volume_level_to_set}%")
    else:
        print("Unsupported platform")

def restore_volume():
    if platform.system() == 'Darwin':
        subprocess.run(["osascript", "-e", "set volume output volume 100"])
    elif platform.system() == 'Windows':
        os.system("nircmd.exe setsysvolume 65535")
    elif platform.system() == 'Linux':
        os.system("amixer set Master 100%")
    else:
        print("Unsupported platform")


def listen_for_keyword(audio_keyword, volume_level):
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print("Listening for keyword...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        transcript = recognizer.recognize_google(audio)
        print(f"You said: {transcript}")
        if audio_keyword.lower() in transcript.lower():
            print("Keyword detected!")
            set_volume(volume_level)
        else:
            print("Keyword not detected.")
            pass
    except sr.UnknownValueError:
        print("Didn't catch that.")
    except sr.RequestError:
        print("Speech recognition service unavailable")


if __name__ == "__main__":
    keyword = input("Enter the keyword to detect: ")
    volume_level = input("Enter the volume level to decrease to (0-100): ")
    while True:
        listen_for_keyword(keyword, int(volume_level))
        time.sleep(1)
