# Project: Resume Parser

**Problem Statement: Resume Parser Application**

Recruiters and HR departments often face challenges when sorting through numerous job applications and resumes. The process can be time-consuming and error-prone, potentially leading to qualified candidates being overlooked. To streamline this process, a web-based resume parser application is proposed.

**Objective:**
The objective of the project is to develop a user-friendly application that allows HR personnel to upload a folder containing resumes in PDF format. The application will parse each resume, extract relevant information such as work history, education, and skills, and categorize the resumes based on the job description specified by the HR. Additionally, the application will assign a relevance score to each resume, aiding in prioritizing candidates. Finally, the parsed resumes will be sorted and renamed for easy reference, and HR can download the downloadable zip file containing the ordered resumes.

**Key Features:**

- **Job Role and Description Specification:** HR provides the job role and description to tailor parsing and scoring criteria.
- **File Upload:** HR uploads a folder of resumes with their names as Role-CandidateName in PDF format.
- **Resume Parsing:** Extraction of key information (work history, education, skills) using NLP and machine learning techniques.
- **Scoring and Prioritization:** Each resume is assigned a relevance score to aid in prioritization, and renamed as Rank-Role-CandidateName.
- **Download ordered resumes:** HR can download a zip file containing ordered resumes.

**Technologies Used:**
The application will be developed using Python for backend processing, Django HTML Templates,CSS,JS for frontend interface, and integrated with Vercel for deployment. Libraries like `pyresparser` will be employed for resume parsing, and SendGrid will handle email notifications securely.

**Outcome:**
The resume parser application aims to significantly reduce manual effort, improve efficiency in candidate evaluation, and enhance HR decision-making by providing a systematic approach to resume screening and prioritization. 

**Pre-Requistics**
Python 3 should be installed

**STEPS**
1. Create a folder named as `resume-parser` and open it in vs code
2. Initialize Git by using `git init` command in terminal
3. Set up virtual environment to isolate project dependencies.
    
    Create virtual environment, folder name can be venv, env, .venv, .env etc.
    ` python -m venv folder-name`
    
    Activate virtual environment, in case getting error in vs code terminal use cmd
    ` folder-name\Scripts\activate`
    
    Activation will install the dependencies downloaded using pip install in the virtual environment
4. Create a `requirements.txt` file
5. Add the dependencies to `requirements.txt`
6. Run command `pip install -r requirements.txt` to install all the dependencies
7. Create Django Project using command `django-admin startproject resume_parser`
8. To run Django Project change to `resume_parser` directory which has `manage.py` and run command `python manage.py runserver`
9. Press `ctrl + C` to stop the running Django Application in terminal
**Please check out the project directory file structure provided in end to understand where to place the directories and files appropriately**
10. Create a folder named `templates`
11. Create a `index.html` file inside `templates` folder
12. Update `'DIRS': ['templates']` in `settings.py` file
12. Create a `views.py` file
13. Update `urls.py` file
14. Test and run Django Project again to ensure `index.html` is loading
**CSS, JS, and images etc. files are placed inside of a static folder in Django Project**
15. Create a `static` folder at same level as of `templates`
16. Create a `css` folder inside static folder
17. Create a `styles.css` file inside css folder
18. Add `{% load static %}` as first line in `index.html`
19. Add `<link rel="stylesheet" href="{% static 'css/styles.css' %}">` in `<head>` tag in `index.html`
20. In `settings.py` add the following
```
STATIC_URL = 'static/'

STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
```
21. Run the command `python manage.py collectstatic` to load static files
22. Run the Django project again using `python manage.py runserver` to test css changes

**Theory and Commands used**

**CMD Commands**

`python --version` -> To check the version of python installed

`mkdir directory-name` -> To create a new folder

`cd directory-name` -> Change Directory

`cd..` -> Return back to parent Directory

`dir /a` -> To view all the files and folder in current directory/folder

`echo. > file-name` -> To create a empty file

`pip install -r requirements.txt` -> Install packages/dependencies mentioned in requirements.txt file

`pip list` -> Displays all installed packages

`pip uinstall package-name` -> Removes installed package

`rmdir /s /q folder-name` -> Removed folder

`/s`: Deletes the specified directory and all its subdirectories (if any).

`/q`: Quiet mode, which suppresses confirmation prompts about whether you are sure you want to delete the directory.

`django-admin startproject project-name` -> Creates a Django Project

`python manage.py runserver` -> Run the Django Project

`python manage.py collectstatic` -> Load static files like CSS, JS, and images etc.

`ctrl + click` -> To go to the url displayed in terminal

`ctrl + c` -> Stop the Django Project

`ctrl + p` -> To search and go to files in project by typing their name

To wrap text with tags in HTML page

Select text to wrap -> `ctrl + shift + p` -> Search `wrap with abbrevation` -> Enter the tag name

`ctrl + shift + v` -> Preview Mark down page (README.md)

`shift + alt + down arrow` -> Duplicate line
