import os
from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import default_storage
from .forms import UploadFileForm
import requests
from urllib.parse import quote


def transcribe_audio(file_path):
    url = "https://bamanankanapi.kabakoo.africa/hackathon/transcribe_to_bam"
    token = "6f13469b-7bf9-4442-ae55-58689acb2c6d"

    with open(file_path, 'rb') as audio_file:
        files = {'file': audio_file}
        data = {'token': token}

        response = requests.post(url, files=files, data=data)

        if response.status_code == 200:
            return response.text
        else:
            return None


def translate_text(transcribed_text, source_lang, target_lang):
    encoded_text = quote(transcribed_text)
    url = f'https://translate.googleapis.com/translate_a/single?client=gtx&sl={source_lang}&tl={target_lang}&dt=t&q={encoded_text}'
    response = requests.get(url)
    translations = []
    if response.ok:
        data = response.json()
        for item in data[0]:
            if item[0]:
                translation = item[0]
                if target_lang == 'ur':
                    translation = translation.replace(", ", "-")
                else:
                    translation = translation.replace(", ", ".")
                translations.append(translation)
    return translations


def get_unsplash_image(query):
    access_key = 'hy7q98UwjGUrQRG2CeEN4C_qHHgWlb5jYVrooR6oyeE'  
    # Générer un identifiant unique basé sur le texte de la requête
    unique_id = hash(query)
    url = f'https://api.unsplash.com/search/photos?query={quote(query)}&client_id={access_key}&id={unique_id}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            image_url = data['results'][0]['urls']['regular']
            return image_url
    return None








def transcribe(request):
    transcription_bambara = None
    translation_bambara = None
    translation_french = None
    image_url = None
    
    if request.method == 'POST' and request.FILES['audio_file']:
        audio_file = request.FILES['audio_file']
        file_path = default_storage.save('tmp/' + audio_file.name, audio_file)
        transcribed_text = transcribe_audio(file_path)
        os.remove(file_path)
        if transcribed_text:
            transcription_bambara = transcribed_text
            translation_bambara = translate_text(transcribed_text, 'bm', 'fr')
            translation_french = translate_text(transcribed_text, 'fr', 'en')
            image_url = get_unsplash_image(" ".join(translation_french))  # Utiliser la traduction en français pour générer l'image
    
    return render(request, 'index.html', {
        'transcription_bambara': transcription_bambara,
        'translation_french': " ".join(translation_french) if translation_french else None,
        'translation_bambara': " ".join(translation_bambara) if translation_bambara else None,
        'image_url': image_url,
    })
# def transcribe(request):
#     transcription_bambara = None
#     translation_bambara = None
#     translation_french = None
#     image_url = None
    
#     if request.method == 'POST' and request.FILES['audio_file']:
#         audio_file = request.FILES['audio_file']
#         file_path = default_storage.save('tmp/' + audio_file.name, audio_file)
#         transcribed_text = transcribe_audio(file_path)
#         os.remove(file_path)
#         if transcribed_text:
#             transcription_bambara = transcribed_text
#             translation_bambara = translate_text(transcribed_text, 'bm', 'fr')
#             translation_french = translate_text(transcribed_text, 'fr', 'fr')
#             image_url = get_unsplash_image(transcribed_text)
    
#     return render(request, 'index.html', {
#         # 'transcription_bambara': transcription_bambara,
#         'translation_french': " ".join(translation_bambara) if translation_french else None,
#         'translation_bambara': " ".join(translation_french) if translation_bambara else None,
#         'image_url': image_url,
#     })

def index(request):
    return render(request, 'index.html')






























# import os
# from django.shortcuts import render
# from django.http import HttpResponse
# from django.core.files.storage import default_storage
# from .forms import UploadFileForm
# import requests
# from urllib.parse import quote


# def transcribe_audio(file_path):
#     url = "https://bamanankanapi.kabakoo.africa/hackathon/transcribe_to_bam"
#     token = "6f13469b-7bf9-4442-ae55-58689acb2c6d"

#     with open(file_path, 'rb') as audio_file:
#         files = {'file': audio_file}
#         data = {'token': token}

#         response = requests.post(url, files=files, data=data)

#         if response.status_code == 200:
#             return response.text
#         else:
#             return None


# def translate_text(transcribed_text, source_lang, target_lang):
#     encoded_text = quote(transcribed_text)
#     url = f'https://translate.googleapis.com/translate_a/single?client=gtx&sl={source_lang}&tl={target_lang}&dt=t&q={encoded_text}'
#     response = requests.get(url)
#     translations = []
#     if response.ok:
#         data = response.json()
#         for item in data[0]:
#             if item[0]:
#                 translation = item[0]
#                 if target_lang == 'ur':
#                     translation = translation.replace(", ", "-")
#                 else:
#                     translation = translation.replace(", ", ".")
#                 translations.append(translation)
#     return translations


# def get_unsplash_image(query):
#     access_key = '6VtCH5Oqz7DNdr41U5bJeOwRU4JeiXjThFCo4M6fBz0'  # Remplacez par votre clé d'API Unsplash
#     url = f'https://api.unsplash.com/search/photos?query={quote(query)}&client_id={access_key}'
#     response = requests.get(url)
#     if response.status_code == 200:
#         data = response.json()
#         if data['results']:
#             image_url = data['results'][0]['urls']['regular']
#             return image_url
#     return None


# def transcribe(request):
#     transcription_bambara = None
#     translation_bambara = None
#     translation_french = None
#     image_url = None
    
#     if request.method == 'POST' and request.FILES['audio_file']:
#         audio_file = request.FILES['audio_file']
#         file_path = default_storage.save('tmp/' + audio_file.name, audio_file)
#         transcribed_text = transcribe_audio(file_path)
#         os.remove(file_path)
#         if transcribed_text:
#             transcription_bambara = transcribed_text
#             translation_bambara = translate_text(transcribed_text, 'bm', 'fr')
#             translation_french = translate_text(transcribed_text, 'fr', 'en')
#             image_url = get_unsplash_image(transcribed_text)
    
#     return render(request, 'index.html', {
#         # 'transcription_bambara': transcription_bambara,
#         'translation_french': " ".join(translation_bambara) if translation_french else None,
#         'translation_bambara': " ".join(translation_french) if translation_bambara else None,
#         'image_url': image_url,
#     })

# def index(request):
#     return render(request, 'index.html')