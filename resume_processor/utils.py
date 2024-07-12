from tika import parser
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from io import BytesIO
import zipfile
import os
import base64
from django.http import HttpResponse, HttpResponseBadRequest
from django.conf import settings

# Load spaCy English model
nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])

def process_resumes(job_description, resume_files):
    """
    Process resume files, calculate similarity scores, and prepare a zip file for download.

    Parameters:
    - job_description (str): The job description text.
    - resume_files (list): List of resume files (UploadedFile instances).

    Returns:
    - HttpResponse: Response object containing the zip file for download.
    """
    try:
        job_description_preprocessed = preprocess_text(job_description)

        # Prepare data structure to store resume content and original file names
        resume_data = []
        resume_file_contents = {}

        for resume_file in resume_files:
            file_content = resume_file.read()
            resume_file_contents[resume_file.name] = file_content

            if resume_file.content_type == 'application/pdf':
                text = extract_pdf_text(BytesIO(file_content))
                preprocessed_text = preprocess_text(text)
                resume_data.append({
                    "filename": resume_file.name,
                    "content": preprocessed_text,
                })
            else:
                resume_data.append({
                    "filename": resume_file.name,
                    "content": f"Unsupported file format: {resume_file.content_type}"
                })

        # Calculate similarity scores
        scores = calculate_similarity(job_description_preprocessed, resume_data)

        # Combine resume data with scores
        for resume, score in zip(resume_data, scores):
            resume['score'] = score

        # Sort resumes by score in descending order
        resume_data.sort(key=lambda x: x['score'], reverse=True)

        # Prepare in-memory zip file with ranked resumes
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w') as zipf:
            # Add job description text file to the zip
            zipf.writestr('job_description.txt', job_description.encode('utf-8'))
            # Add ranked resumes to the zip
            for idx, resume in enumerate(resume_data):
                original_filename = resume['filename']
                ranked_filename = f"{idx + 1} {original_filename}"
                zipf.writestr(ranked_filename, resume_file_contents[original_filename])

        # Serve the zip file as a download response
        zip_buffer.seek(0)
        response = HttpResponse(zip_buffer.getvalue(), content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="ranked_resumes.zip"'

    except Exception as e:
        print(f"Error processing resumes: {str(e)}")
        response = HttpResponseBadRequest("Error processing resumes")

    return response

def extract_pdf_text(pdf_file):
    raw = parser.from_buffer(pdf_file)
    return raw.get('content', '')

def preprocess_text(text):
    # Preprocessing steps using spaCy for tokenization and stopword removal
    doc = nlp(text.lower().replace('\n',''))  # Tokenize and lowercase
    filtered_text = [token.text for token in doc if not token.is_stop and token.is_alpha]
    return " ".join(filtered_text)

def calculate_similarity(job_description, resume_data):
    # Extract all texts
    all_texts = [job_description] + [resume['content'] for resume in resume_data]

    # Initialize TF-IDF vectorizer
    tfidf_vectorizer = TfidfVectorizer()

    # Fit-transform to get TF-IDF vectors
    tfidf_vectors = tfidf_vectorizer.fit_transform(all_texts)

    # Calculate cosine similarity between job description and resumes
    job_description_vector = tfidf_vectors[0]
    resume_vectors = tfidf_vectors[1:]

    similarities = cosine_similarity(job_description_vector, resume_vectors)
    scores = similarities.flatten()

    return scores.tolist()

def load_demo_data():
    # Path to demo data
    demo_data_path = os.path.join(settings.BASE_DIR, 'resume_processor', 'static', 'demo-data')

    # Load job description
    with open(os.path.join(demo_data_path, 'job_description.txt'), 'r', encoding='utf-8') as file:
        job_description = file.read()

    # Load resumes
    resume_files = []
    for filename in os.listdir(demo_data_path):
        if filename.endswith('.pdf'):
            with open(os.path.join(demo_data_path, filename), 'rb') as file:
                resume_files.append({
                    'filename': filename,
                    'content': base64.b64encode(file.read()).decode('utf-8'),
                })

    return {'job_description': job_description, 'resume_files': resume_files}
