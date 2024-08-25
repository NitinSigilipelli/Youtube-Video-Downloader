import os
import speech_recognition as sr
from pytube import YouTube
from pydub import AudioSegment

# Step 1: Download the audio from the YouTube video
def download_audio_from_youtube(video_url, output_path='audio.mp3'):
    yt = YouTube(video_url)
    audio_stream = yt.streams.filter(only_audio=True).first()
    downloaded_file = audio_stream.download(filename='video_audio')
    base, ext = os.path.splitext(downloaded_file)
    new_file = base + '.mp3'
    os.rename(downloaded_file, new_file)
    return new_file

# Step 2: Convert audio to WAV format (required by SpeechRecognition)
def convert_audio_to_wav(input_audio_path, output_wav_path='audio.wav'):
    audio = AudioSegment.from_file(input_audio_path)
    audio.export(output_wav_path, format='wav')
    return output_wav_path

# Step 3: Transcribe audio to text
def transcribe_audio_to_text(wav_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_path) as audio_file:
        audio_content = recognizer.record(audio_file)
        try:
            text = recognizer.recognize_google(audio_content)
            return text
        except sr.UnknownValueError:
            return "Google Speech Recognition could not understand the audio"
        except sr.RequestError as e:
            return f"Could not request results from Google Speech Recognition service; {e}"

# Main function
if __name__ == "__main__":
    video_url = 'https://www.youtube.com/watch?v=YOUR_VIDEO_ID'  # Replace with your video URL
    audio_file_path = download_audio_from_youtube(video_url)
    wav_file_path = convert_audio_to_wav(audio_file_path)
    transcription = transcribe_audio_to_text(wav_file_path)
    
    print("Transcribed Text:\n")
    print(transcription)
