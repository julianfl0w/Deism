# import pyttsx3
# engine = pyttsx3.init()
# engine.say("I will speak this text")
# engine.runAndWait()

from gtts import gTTS

tts = gTTS(text="what to say", lang="en")
tts.save("file.mp3")
