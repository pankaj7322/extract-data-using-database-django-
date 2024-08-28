from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.views.decorators.csrf import csrf_exempt
import speech_recognition as sr

from django.core.files.base import ContentFile
import json
import os
import sqlite3
from transformers import WhisperForConditionalGeneration, WhisperProcessor
import torchaudio
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM 

from pydub import AudioSegment
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import speech_recognition as sr
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView


def homepage(request):
    return render(request, 'homepage.html')
#################################################################
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import JsonResponse
import os


# Load the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("juierror/flan-t5-text2sql-with-schema-v2")
model1 = AutoModelForSeq2SeqLM.from_pretrained("juierror/flan-t5-text2sql-with-schema-v2")

def get_prompt(tables, question):
    prompt = f"convert question and table into SQL query. tables: {tables}. question: {question}"
    return prompt
def prepare_input(question: str, tables: dict[str, list[str]]):
    tables = [f"{table_name}({','.join(tables[table_name])})" for table_name in tables]
    tables = ", ".join(tables)
    prompt = get_prompt(tables, question)
    
    # Explicitly enable truncation
    input_ids = tokenizer(prompt, max_length=512, truncation=True, return_tensors="pt").input_ids
    return input_ids

def inference(question: str, tables: dict[str, list[str]]) -> str:
    input_data = prepare_input(question=question, tables=tables)
    input_data = input_data.to(model1.device)
    outputs = model1.generate(inputs=input_data, num_beams=10, max_length=512)
    result = tokenizer.decode(token_ids=outputs[0], skip_special_tokens=True)
    return result

def sql_query_view(request):
    pass
        # Define your table schema here or fetch dynamically as needed
        

        # Generate SQL query using the inference function
        


# *******************************************************************************************

# def login_view(request):
#     if request.method == "POST":
#         username = request.POST['username']
#         password = request.POST['password']

#         if username == 'testuser' and password == 'testpass':

#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect('index')  # Redirect to the form page after login
#             else:
#                return render(request, 'login.html', {'error': 'Invalid credentials'})
#         else:
#             return render(request, 'login.html')
#     return render(request, 'login.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        print(f"Attempting login for {username}")  # Debug statement
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print(f"Login successful for {username}")  # Debug statement
            return redirect('index')
        else:
            print(f"Login failed for {username}")  # Debug statement
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')


@login_required
def index(request):
    return render(request, 'index.html')

#####################################
@login_required
def submit_form(request):
    if request.method == 'POST':
        question = request.POST.get('input_text', '')

        tables = {"employees": ["name", "age", "department", "salary"]}

        sql_query = inference(question, tables)
        conn = sqlite3.connect('employee_database.db')
        cursor = conn.cursor()
        results = []
        error_message = None

        try:
            cursor.execute(sql_query)
            results = cursor.fetchall()
        except sqlite3.Error as e:
            error_message = f"An Error occurred: {e}"

        conn.commit()
        conn.close()

        # Render results in a new template
        return render(request, 'results.html', {
            'sql_query': sql_query,
            'results': results,
            'error_message': error_message,
        })

    # If GET request, render the initial form
    return render(request, 'submit_form.html')
###########################################



###########################################

@csrf_exempt
def record_audio(request):
    if request.method == 'POST' and request.FILES.get('audio'):
        audio_file = request.FILES['audio']
        file_name = 'recording.mp3'
        
        # Save the file to the MEDIA folder
        file_path = default_storage.save(os.path.join('media', file_name), ContentFile(audio_file.read()))
        file_url = default_storage.url(file_path)


        # Full path of the saved audio file
        full_file_path = os.path.join(default_storage.location, file_path)

        #Load the whisper model and processor from Hugging Face

        model_name = "openai/whisper-small"
        model = WhisperForConditionalGeneration.from_pretrained(model_name)
        processor = WhisperProcessor.from_pretrained(model_name)

        audio_input, _ =  torchaudio.load(full_file_path)

        inputs = processor(audio_input.squeeze().numpy(), return_tensors = "pt", sampling_rate = 16000)

        with torch.no_grad():
            logits = model(**inputs).logits

        # Decode the transcription
        predicted_ids = torch.argmax(logits, dim=-1)
        transcription = processor.decode(predicted_ids[0])
        
        return JsonResponse({'status': 'success', 'file_url': file_url, 'transcription': file_url})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)



# *************************************************************************************************

# from django.core.files.storage import default_storage
# from django.core.files.base import ContentFile
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# import os

# # Import Whisper model from Hugging Face transformers library
# from transformers import pipeline

# # Load Whisper model (make sure you have the correct model installed)
# whisper_model = pipeline("automatic-speech-recognition", model="openai/whisper-base")

# @csrf_exempt
# def record_audio(request):
#     if request.method == 'POST' and request.FILES.get('audio'):
#         audio_file = request.FILES['audio']
#         file_name = 'recording.wav'
        
#         # Save the file to the MEDIA folder
#         file_path = default_storage.save(os.path.join('media', file_name), ContentFile(audio_file.read()))
#         file_url = default_storage.url(file_path)
        
#         # Full path of the saved audio file
#         full_file_path = os.path.join(default_storage.location, file_path)

#         # Use Whisper model to transcribe the audio file
#         try:
#             result = whisper_model(full_file_path)
#             transcription = result['text']
#         except Exception as e:
#             return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

#         return JsonResponse({'status': 'success', 'file_url': file_url, 'transcription': transcription})
    
#     return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)




# ****************************************************************************************************

# def record_audio(request):
#     if request.method == 'POST' and 'audio' in request.FILES:
#         audio_file  = request.FILES['audio']

#         recognizer = sr.Recognizer()

#         with sr.AudioFile(audio_file) as source:
#             audio = recognizer.record(source)

#         try:
#             transcription = recognizer.recognize_google(audio)
#         except sr.UnknownValueError:
#             transcription = "Google will not understand your voice"
#         except sr.RequestError as e:
#             transcription = f"Could not request from google web Speech API {e}"

#          # Print the transcription to the command line
#         print(f"Transcription: {transcription}")

#         return JsonResponse({'transcription:', transcription})

#     return JsonResponse({'error': 'Invalid Request'} ,status = 400)

