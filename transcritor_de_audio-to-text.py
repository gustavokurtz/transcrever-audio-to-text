# transcritor_de_audio_mp3.py

import speech_recognition as sr
from pydub import AudioSegment
from pydub.utils import which
import os
from tkinter import Tk, filedialog

# Configurar o ffmpeg para pydub
AudioSegment.converter = which("ffmpeg")

def convert_mp3_to_wav(mp3_path, wav_path):
    audio = AudioSegment.from_mp3(mp3_path)
    audio.export(wav_path, format="wav")

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

def select_file():
    root = Tk()
    root.withdraw()  # Esconde a janela principal
    file_path = filedialog.askopenfilename(
        title="Selecione o arquivo de áudio MP3",
        filetypes=[
            ("Arquivos de áudio MP3", "*.mp3")
        ]
    )
    return file_path

if __name__ == "__main__":
    print("Bem-vindo ao transcritor de áudio MP3 para texto.")
    print("Extensões suportadas: .mp3")
    print("Por favor, evite arquivos muito longos (acima de algumas centenas de megabytes) devido a limitações de memória.")
    
    file_path = select_file()
    if not file_path:
        print("Nenhum arquivo selecionado.")
    elif not os.path.exists(file_path):
        print(f"O caminho fornecido não existe: {file_path}")
    else:
        try:
            wav_path = "converted_audio.wav"
            print("Convertendo MP3 para WAV...")
            convert_mp3_to_wav(file_path, wav_path)
            print("Arquivo convertido com sucesso.")
            
            text = transcribe_audio(wav_path)
            with open("transcription.txt", "w", encoding="utf-8") as f:
                f.write(text)
            print("Transcrição concluída e salva em 'transcription.txt'.")
            os.remove(wav_path)
        except Exception as e:
            print(f"Ocorreu um erro ao processar o arquivo: {e}")
