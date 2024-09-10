from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.views.decorators.csrf import csrf_exempt
import speech_recognition as sr
import soundfile as sf
from typing import List,Dict

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
model = AutoModelForSeq2SeqLM.from_pretrained("juierror/flan-t5-text2sql-with-schema-v2")

# Function to create the prompt
def get_prompt(tables, question):
    prompt = f"convet question and table into SQL query. tables: {tables}. question: {question}"
    return prompt

# Function to prepare input for the model
def prepare_input(question: str, tables: Dict[str, List[str]]):
    # Format table information
    table_name = list(tables.keys())[0]
    columns = tables[table_name]
    tables_str = f"{table_name}({','.join(columns)})"
    prompt = get_prompt(tables_str, question)
    input_ids = tokenizer(prompt, max_length=512, truncation=True, return_tensors="pt").input_ids
    return input_ids

# Function to perform inference and get SQL query
def inference(question: str, tables: Dict[str, List[str]]) -> str:
    input_data = prepare_input(question=question, tables=tables)
    input_data = input_data.to(model.device)
    outputs = model.generate(input_ids=input_data, num_beams=5, max_length=512)
    result = tokenizer.decode(token_ids=outputs[0], skip_special_tokens=True)
    return result


def sql_query_view(request):
    pass
        # Define your table schema here or fetch dynamically as needed
        

        # Generate SQL query using the inference function
        

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
        question = request.POST.get('input_text')

        tables = {"employees": ["id", "name", "age","department", "salary"]}

        sql_query = inference(question, tables)
        print("question question", question)
        print("sql sql sql", sql_query)
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
def audio_to_text(file_path):
    # Convert audio to WAV format
    sound = AudioSegment.from_file(file_path)
    wav_path = file_path.replace('.mp3', '.wav')
    sound.export(wav_path, format='wav')

    # Use SpeechRecognition to convert to text
    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_path) as source:
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data)

    # Clean up
    os.remove(wav_path)

    return text



def upload_audio(request):
    transcription = None
    if request.method == 'POST' and request.FILES.get('audio_file'):
        audio_file = request.FILES['audio_file']
        file_name = 'uploaded_audio.wav'

        # Save the file to the media folder
        file_path = default_storage.save(os.path.join('media', file_name), ContentFile(audio_file.read()))

        # Get the full path of the saved file
        full_file_path = os.path.join(default_storage.location, file_path)

        result = audio_to_text(full_file_path)

        # Convert audio to text using Whisper
        transcription = result

    return render(request, 'index.html', {'transcription': transcription})
