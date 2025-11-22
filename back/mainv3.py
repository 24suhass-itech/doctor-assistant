import speech_recognition as sr
from predictv3 import diagnose
import os

def speak(text):
    os.system(f'mshta "javascript:var t=new ActiveXObject(\'SAPI.SpVoice\'); t.Speak(\'{text}\');close()"')

r = sr.Recognizer()

print("🎤 Speak your symptoms now...")

with sr.Microphone() as mic:
    print("Calibrating mic...")
    r.adjust_for_ambient_noise(mic, duration=1)

    r.energy_threshold = 100  # more sensitive
    r.dynamic_energy_threshold = False

    print("Listening...")
    audio = r.listen(mic, timeout=5, phrase_time_limit=10)

print("🛰 Transcribing with Google...")

try:
    text = r.recognize_google(audio)
    print("📝 You said:", text)

    disease = diagnose(text)
    print("🤒 Detected Disease:", disease)

    speak(f"You may have {disease}")

except sr.UnknownValueError:
    print("❌ Could not understand audio")
    speak("I could not understand you")

except sr.RequestError:
    print("❌ Google Speech recognition service failed")
    speak("Speech service is not available")
