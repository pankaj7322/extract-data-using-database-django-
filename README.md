# Extract Data Using Database Using Django

This project demonstrates how to build a Django web application that extracts data from a database using natural language input. Users can interact with the application to query a SQLite database by providing a question in plain English. The app translates the natural language input into a SQL query using a pretrained model, fetches the data from the database, and displays the results. Additionally, users can upload audio files which are transcribed into text and can also be used for querying the database.

## Features

- **User Authentication**: Login system to allow users access to query the database.
- **Natural Language Querying**: Users input questions in plain English, which are translated into SQL queries using a pretrained model.
- **Audio Transcription**: Users can upload an audio file (MP3) that is converted into text and used for database queries.
- **SQLite Database**: The app uses an SQLite database (`employee_database.db`) to store and query employee data.
- **SQL Query Execution**: SQL queries are executed based on user input, and the results are displayed on the results page.

## Technologies Used

- **Django**: Web framework for building the application.
- **Transformers (Hugging Face)**: For natural language to SQL query conversion using the `juierror/flan-t5-text2sql-with-schema-v2` model.
- **SpeechRecognition**: For converting audio files to text using Google's Speech-to-Text API.
- **Pydub**: For handling audio format conversions (MP3 to WAV).
- **SQLite**: For storing and querying employee data.
- **Whisper**: Optional integration to transcribe audio input into text.

## Setup Instructions

### Prerequisites

- Python 3.x
- Django 4.x
- SQLite
- Pytorch (for Hugging Face model)
- `transformers` and `torch` libraries from Hugging Face

### Installation Steps

1. **Clone the Repository**

    ```bash
    git clone https://github.com/yourusername/extract-data-using-database.git
    cd extract-data-using-database
    ```

2. **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

3. **Apply Migrations**

    ```bash
    python manage.py migrate
    ```

4. **Run the Server**

    ```bash
    python manage.py runserver
    ```

5. **Access the Application**

    Open your browser and navigate to `http://127.0.0.1:8000/`.

### Database Setup

The app currently uses a SQLite database to store employee data. The schema includes a table called `employees` with the following fields:

- `id` (integer)
- `name` (text)
- `age` (integer)
- `department` (text)
- `salary` (integer)

You can customize the schema to match your specific database structure.

### Configuring Audio Transcription

This app uses Google's Speech-to-Text API via the `speech_recognition` library to transcribe uploaded audio files. To use this feature:

- Ensure that the file you upload is in MP3 format.
- The transcription is processed, and the text is used to generate SQL queries.

### Folder Structure

```plaintext
extract-data-using-database/
│
├── app/                   # Django app files
│   ├── migrations/        # Migration files for database
│   ├── static/            # Static files (CSS, JS)
│   ├── templates/         # HTML templates
│   ├── models.py          # Database models
│   ├── views.py           # Application views (business logic)
│   └── urls.py            # URL routing
│
├── media/                 # Directory where uploaded files are stored
├── db.sqlite3             # SQLite database (auto-generated)
├── manage.py              # Django management script
├── requirements.txt       # Project dependencies
└── README.md              # Project documentation
