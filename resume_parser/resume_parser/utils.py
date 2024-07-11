from tika import parser
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from io import BytesIO
import os
import zipfile
from django.http import HttpResponse, HttpResponseBadRequest


nltk.download('punkt')
nltk.download('stopwords')

def process_resumes(job_description, resume_files):
    """
    Process resume files, calculate similarity scores, and prepare a zip file for download.

    Parameters:
    - job_description (str): The job description text.
    - resume_files (list): List of resume files (UploadedFile instances).

    Returns:
    - HttpResponse: Response object containing the zip file for download.
    """
    zip_filename = 'ranked_resumes.zip'
    try:
        # Write job description to a temporary text file
        job_description_filename = 'job_description.txt'
        with open(job_description_filename, 'w', encoding='utf-8') as job_desc_file:
            job_desc_file.write(job_description)

        job_description_preprocessed = preprocess_text(job_description)

        # Prepare data structure to store resume content and original file names
        resume_data = []
        resume_file_contents = {}  # Dictionary to store file content
        
        for resume_file in resume_files:
            file_content = resume_file.read()  # Read file content once
            resume_file_contents[resume_file.name] = file_content  # Store content
            
            if resume_file.content_type == 'application/pdf':
                text = extract_pdf_text(BytesIO(file_content))  # Extract text from PDF
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

        # Prepare zip file with ranked resumes and job description
        with zipfile.ZipFile(zip_filename, 'w') as zipf:
            # Add job description text file to the zip
            zipf.write(job_description_filename, os.path.basename(job_description_filename))
            
            # Add ranked resumes to the zip
            for idx, resume in enumerate(resume_data):
                original_filename = resume['filename']
                ranked_filename = f"{idx + 1} {original_filename}"
                zipf.writestr(ranked_filename, resume_file_contents[original_filename])

        # Serve the zip file as a download response
        with open(zip_filename, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/zip')
            response['Content-Disposition'] = f'attachment; filename="{zip_filename}"'

    except Exception as e:
        # Handle exceptions and return an error response
        print(f"Error processing resumes: {str(e)}")
        response = HttpResponseBadRequest("Error processing resumes")

    finally:
        # Clean up - delete the temporary files from the server
        try:
            os.remove(zip_filename)
            os.remove(job_description_filename)
        except Exception as e:
            print(f"Error cleaning up: {str(e)}")

    return response

def extract_pdf_text(pdf_file):
    raw = parser.from_buffer(pdf_file)
    return raw['content']

def preprocess_text(text):
    # Preprocessing steps
    cleaned_text = text.lower().replace('\n', '')  # Convert to lowercase and remove new lines
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