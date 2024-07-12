# Project: Resume Prioritizer

**Problem Statement: Resume Prioritizer Application**

Recruiters and HR departments often face challenges when sorting through numerous job applications and resumes. The process can be time-consuming and error-prone, potentially leading to qualified candidates being overlooked. To streamline this process, a web-based resume prioritizer application is proposed.

**Objective:**
The objective of the project is to develop a user-friendly application that allows HR personnel to upload a folder containing resumes in PDF format. The application will parse each resume, extract relevant information such as work history, education, and skills, and categorize the resumes based on the job description specified by the HR. Additionally, the application will assign a relevance score to each resume, aiding in prioritizing candidates. Finally, the parsed resumes will be sorted and renamed for easy reference, and HR can download a zip file containing the ordered resumes.

**Key Features:**

- **Job Role and Description Specification:** HR provides the job role and description to tailor parsing and scoring criteria.
- **File Upload:** HR uploads a folder of resumes with their names as Role-CandidateName in PDF format.
- **Resume Parsing:** Extraction of key information (work history, education, skills) using NLP and machine learning techniques.
- **Scoring and Prioritization:** Each resume is assigned a relevance score to aid in prioritization, and renamed as Rank-Role-CandidateName.
- **Download ordered resumes:** HR can download a zip file containing ordered resumes.

**Technologies Used:**
The application will be developed using Python for backend processing, HTML/CSS for frontend interface, and integrated with Vercel for deployment. Used packages like `django`, `tika`, `textblob` etc. as specified in `requirements.txt`

**Outcome:**
The application takes in job description as text input and resumes in pdf file format and produces a zip folder with ranked resumes based on the best match of the role.
The resume prioritizer application aims to significantly reduce manual effort, improve efficiency in candidate evaluation, and enhance HR decision-making by providing a systematic approach to resume screening and prioritization. 

**Project Demo**
## Watch the Demo

[![Watch the video here](/demo_thumbnail.png)](/video_demo.gif)

![Video Demo GIF](/video_demo.gif)

Note: Demo video attached in repository.

**Pre-Requistics**

Python 3 should be installed

**How to run this project locally**

The below code will help you run the code in your local computer.

Create a folder and run the following commands in CMD/terminal to run the project locally.

```
git clone https://github.com/harsha123e/resume-prioritizer.git
cd resume-prioritizer
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py runserver
```

Ctrl + Click on the link provided in CMD/terminal to open the application.

**Understanding the above commands**

`git clone https://github.com/harsha123e/resume-prioritizer.git` -> Create a clone/copy of the project locally

`cd resume-prioritizer` -> Change to project's directory

`python -m venv venv` -> Create a virtual environment

`venv\Scripts\activate` -> Activate the virtual environment

`pip install -r requirements.txt` -> Install the needed dependencies/packages to run the project

`python manage.py runserver` -> Start the Django server to run the project locally

**Understanding folder structure**
```
resume_parser
resume_parser\__pycache__              -- Compiled bytecode files for performance
resume_parser\__init__.py              -- Marks directory as a Python package
resume_parser\asgi.py                  -- ASGI configuration for asynchronous support
resume_parser\settings.py              -- Django project settings and configurations
resume_parser\urls.py                  -- URL routing for the project
resume_parser\wsgi.py                  -- WSGI configuration for web server

resume_processor
resume_processor\__pycache__           -- Compiled bytecode files for performance
resume_processor\static                -- Store static files like images, CSS, and JS
resume_processor\static\css            -- CSS files
resume_processor\static\demo-data      -- Sample resume data for demonstration
resume_processor\static\favicons       -- Favicon images
resume_processor\static\images         -- Image files
resume_processor\static\js             -- JavaScript files
resume_processor\templates             -- HTML template files
resume_processor\templates\base.html   -- Base template to be extended by other templates
resume_processor\templates\home.html   -- Home page template
resume_processor\templates\modal.html  -- Modal popup template
resume_processor\apps.py               -- App configuration
resume_processor\urls.py               -- URL routing for the app
resume_processor\utils.py              -- Utility functions for the app
resume_processor\views.py              -- View functions handling HTTP requests

staticfiles                            -- Collects all static files for production
.gitignore                             -- Specifies files and directories for Git to ignore
build.sh                               -- Shell script to build or deploy the project
demo_thumbnail.png                     -- Thumbnail image for demo of project
manage.py                              -- Command-line utility to interact with the project
README.md                              -- Project description and documentation
requirements.txt                       -- Lists Python packages required for the project
video.webm                             -- Video file demo of project
```
