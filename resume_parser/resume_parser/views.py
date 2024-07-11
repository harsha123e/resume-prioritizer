import os
import zipfile
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from tika import parser
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from io import BytesIO

nltk.download('punkt')
nltk.download('stopwords')

def index_view(request):
    return render(request, 'index.html')

@csrf_exempt
@require_POST
def upload_view(request):
    if request.method == "POST":
        job_description = request.POST.get("jobDescription", "")
        job_description = preprocess_text(job_description)
        resume_files = request.FILES.getlist("resumeFolder")

        # Prepare data structure to store resume content and original file names
        resume_data = []
        resume_file_contents = {}  # Dictionary to store file content
        
        for resume_file in resume_files:
            file_content = resume_file.read()  # Read file content once
            resume_file_contents[resume_file.name] = file_content  # Store content
            
            if resume_file.content_type == 'application/pdf':
                text = extract_pdf_text(BytesIO(file_content))  # Pass BytesIO object to extract text
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
        scores = calculate_similarity(job_description, resume_data)

        # Combine resume data with scores
        for resume, score in zip(resume_data, scores):
            resume['score'] = score

        # Sort resumes by score in descending order
        resume_data.sort(key=lambda x: x['score'], reverse=True)

        # Rename and zip resumes based on ranking
        zip_filename = 'ranked_resumes.zip'
        with zipfile.ZipFile(zip_filename, 'w') as zipf:
            for idx, resume in enumerate(resume_data):
                original_filename = resume['filename']
                ranked_filename = f"{idx + 1} {original_filename}"
                zipf.writestr(ranked_filename, resume_file_contents[original_filename])
                print(f"Added {ranked_filename} to {zip_filename}")

        # Serve the zip file as a download response
        with open(zip_filename, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/zip')
            response['Content-Disposition'] = f'attachment; filename="{zip_filename}"'

        # Clean up - delete the zip file from the server
        os.remove(zip_filename)

        return response

    return HttpResponseBadRequest("Invalid request method")

def extract_pdf_text(pdf_file):
    raw = parser.from_buffer(pdf_file)
    return raw['content']

def preprocess_text(text):
    # Example preprocessing steps (you can modify or add more steps as needed)
    cleaned_text = text.lower()  # Convert to lowercase
    tokens = word_tokenize(cleaned_text)  # Tokenize text into words
    stop_words = set(stopwords.words('english'))
    filtered_text = [word for word in tokens if word not in stop_words]  # Remove stopwords
    
    return " ".join(filtered_text)  # Return preprocessed text as a string

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
