from django.shortcuts import render

def index_view(request):
    return render(request, 'index.html')

from django.http import HttpResponseBadRequest, HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt  # Only for testing; use proper CSRF protection in production
@require_POST
def upload_view(request):
    if request.method == "POST":
        job_description = request.POST.get("jobDescription", "")
        resume_files = request.FILES.getlist("resumeFolder")

        # Process job description and resume files here
        # Example: Save files or perform operations based on job description

        # For demo purposes, let's create a dummy zip file as response
        import zipfile
        from io import BytesIO

        # Create a zip file containing dummy data
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zip_file:
            for index, resume_file in enumerate(resume_files):
                zip_file.writestr(f"resume_{index}.txt", resume_file.read())

        # Prepare HTTP response with zip file
        response = HttpResponse(zip_buffer.getvalue(), content_type="application/zip")
        response["Content-Disposition"] = 'attachment; filename="ranked_resumes.zip"'
        return response

    return HttpResponseBadRequest("Invalid request method")
