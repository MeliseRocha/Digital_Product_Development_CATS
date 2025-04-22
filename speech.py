# import speech_recognition as sr


# recognizer = sr.Recognizer()

# with sr.AudioFile('/home/melise/Downloads/e16a32e9-15a7-4c14-b831-5f0eb7f2a6ae.wav') as source:
#     audio_data = recognizer.record(source)

# text = recognizer.recognize_google(audio_data)
# print(text)
import whisper

model = whisper.load_model("base")
result = model.transcribe("/home/melise/Downloads/e16a32e9-15a7-4c14-b831-5f0eb7f2a6ae.webm")
print(result["text"])

