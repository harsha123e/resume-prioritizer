
from django.shortcuts import render
from django.http import HttpResponseBadRequest
from django.views.decorators.http import require_POST
from .utils import process_resumes, load_demo_data
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
    try:
        demo_data = load_demo_data()
        return JsonResponse(demo_data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)