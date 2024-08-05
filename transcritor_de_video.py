# transcritor_de_video.py

import moviepy.editor as mp
import speech_recognition as sr
import os
from tkinter import Tk, filedialog

def extract_audio(video_path, audio_path):
    video = mp.VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path)

def transcribe_audio(audio_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio, language="pt-BR")
        return text
    except sr.UnknownValueError:
        return "Google Speech Recognition could not understand audio"
    except sr.RequestError as e:
        return f"Could not request results from Google Speech Recognition service; {e}"

def transcribe_video_to_text(video_path):
    audio_path = "extracted_audio.wav"
    extract_audio(video_path, audio_path)
    text = transcribe_audio(audio_path)
    os.remove(audio_path)
    return text

def select_file():
    root = Tk()
    root.withdraw()  # Esconde a janela principal
    video_path = filedialog.askopenfilename(
        title="Selecione o vídeo",
        filetypes=[
            ("Todos os arquivos de vídeo", "*.mp4;*.avi;*.mov;*.mkv;*.flv"),
            ("MP4 files", "*.mp4"),
            ("AVI files", "*.avi"),
            ("MOV files", "*.mov"),
            ("MKV files", "*.mkv"),
            ("FLV files", "*.flv")
        ]
    )
    return video_path

if __name__ == "__main__":
    print("Bem-vindo ao transcritor de vídeo para texto.")
    print("Extensões de vídeo suportadas: .mp4, .avi, .mov, .mkv, .flv")
    print("Por favor, evite vídeos muito longos (acima de algumas centenas de megabytes) devido a limitações de memória.")
    
    video_path = select_file()
    if not video_path:
        print("Nenhum arquivo selecionado.")
    elif not os.path.exists(video_path):
        print(f"O caminho fornecido não existe: {video_path}")
    else:
        try:
            text = transcribe_video_to_text(video_path)
            with open("transcription.txt", "w", encoding="utf-8") as f:
                f.write(text)
            print("Transcrição concluída e salva em 'transcription.txt'.")
        except Exception as e:
            print(f"Ocorreu um erro ao processar o vídeo: {e}")


## Audios de até 2min