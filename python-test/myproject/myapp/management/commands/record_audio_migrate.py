# Import des bibliothèques nécessaires
import subprocess
import pyaudio
import wave
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Appliquer les migrations de la base de données et enregistrer l\'audio'

    def handle(self, *args, **options):
        # Appliquer les migrations
        subprocess.call(['python', 'manage.py', 'migrate'])

        # Paramètres d'enregistrement audio
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100
        CHUNK = 1024
        RECORD_SECONDS = 5

        # Créer un objet PyAudio
        p = pyaudio.PyAudio()

        # Ouvrir un flux audio
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        # Afficher un message pour indiquer que l'enregistrement démarre
        print("Enregistrement audio en cours...")

        # Enregistrer l'audio
        frames = []
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)
        
        # Arrêter le flux et fermer PyAudio
        stream.stop_stream()
        stream.close()
        p.terminate()

        # Écrire les données audio dans un fichier WAV
        with wave.open('recorded_audio.wav', 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))

        # Afficher un message pour indiquer que l'enregistrement est terminé
        print("Enregistrement audio terminé.")
