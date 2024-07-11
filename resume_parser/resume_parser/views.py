
from django.shortcuts import render
from django.http import HttpResponseBadRequest
from django.views.decorators.http import require_POST
from .utils import process_resumes
import os
import base64
from django.conf import settings
from django.http import JsonResponse

def index_view(request):
    return render(request, 'index.html')

@require_POST
def upload_view(request):
    if request.method == "POST":
        job_description = request.POST.get("jobDescription", "")
        resume_files = request.FILES.getlist("resumeFolder")

        return process_resumes(job_description, resume_files)

    return HttpResponseBadRequest("Invalid request method")

def load_demo_data_view(request):
    # Path to demo data
    demo_data_path = os.path.join(settings.STATIC_ROOT, 'demo-data')

    # Load job description
    with open(os.path.join(demo_data_path, 'job_description.txt'), 'r') as file:
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

    return JsonResponse({'job_description': job_description, 'resume_files': resume_files})