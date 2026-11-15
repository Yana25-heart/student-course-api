# STUDENT COURSE API

**Laboratory Activity 3A - Creating a Backend API**
Student: (write your name here)
Course: System Integration and Architecture

A small, read-only REST API built with Python and Flask. It returns six
fictional university courses that live inside app.py. No database, no login,
no written code path that changes data - just three GET endpoints.

---

## 1. What is an API?

API stands for Application Programming Interface. In web development it means a
service that answers HTTP requests with data instead of a web page.

You send a request to a URL. The server answers with:

- a status code, such as 200 (OK) or 404 (not found)
- a body, usually JSON text
- headers, such as Content-Type: application/json

An API is how two systems talk to each other. A mobile app, a classmate's
website, a spreadsheet script and Postman can all call the same API and receive
the same data. That is the whole idea behind System Integration: independent
systems agree on a contract (paths, methods, response shapes) and integrate
through it.

Vocabulary used in this laboratory:

- Endpoint - one URL the API answers, for example /api/courses
- Method - the action being asked for. This API allows GET only (read).
- Status code - 200 means OK, 404 means the thing you asked for is missing.
- JSON - the text format used for every response body.
- CORS - the rules a browser follows before it lets a web page call another server.

---

## 2. What each file does

**app.py**
The application itself. It creates the Flask app, switches on CORS, stores the
six example courses in a Python list, and defines one function per endpoint plus
two error handlers. This is the file Render runs.

**requirements.txt**
The shopping list of libraries Render installs before starting the app: Flask
(the framework), Flask-Cors (browser access) and Gunicorn (the production web
server). Each version is pinned so the build is repeatable.

**README.md**
This document: what the project is, how to run it, how to test it, and how it
was deployed. Any marker or teammate reads this first.

---

## 3. The endpoints

GET /api/health
    Returns {"status": "success", "message": "Student Course API is running"}
    Use it to check that the service is awake.

GET /api/courses
    Returns a JSON array of six course objects. Each has an integer id, a
    course code, a course name and a short description.

GET /api/courses/<id>
    Returns the single matching course object.
    If the id does not exist, returns HTTP 404 with a JSON error that lists the
    ids that do exist.

Every response is JSON. Nothing in this API writes data.

---

## 4. Run it on your own computer

    pip install -r requirements.txt
    python app.py

Then open http://localhost:5000/api/health in a browser.

---

## 5. How to test the endpoints

In a browser (fastest):

    http://localhost:5000/api/health
    http://localhost:5000/api/courses
    http://localhost:5000/api/courses/2
    http://localhost:5000/api/courses/99

With curl, in a terminal:

    curl http://localhost:5000/api/health
    curl http://localhost:5000/api/courses
    curl -i http://localhost:5000/api/courses/2
    curl -i http://localhost:5000/api/courses/99

curl -i also prints the status line and headers, which is the easiest way to
show a 404 in your documentation.

With Postman or Thunder Client:

1. Create a new request and choose GET.
2. Paste the URL, for example http://localhost:5000/api/courses
3. Press Send and look at the status code and the Body tab.

On Render, use exactly the same paths with your service address, for example:

    https://student-course-api.onrender.com/api/courses

---

## 6. Push the code to GitHub

1. Sign in at github.com (create an account if needed).
2. Click New repository. Name it student-course-api. Choose Public.
   Do not add a README, .gitignore or licence - the files already exist.
3. Click Create repository.
4. On the empty repository page choose "uploading an existing file".
5. Drag in app.py, requirements.txt and README.md, then click Commit changes.
6. Open the green Code button and copy the repository HTTPS URL.
   Render needs that URL.

Optional, with Git installed instead of the browser upload:

    git init
    git add .
    git commit -m "Student Course API - Laboratory Activity 3A"
    git branch -M main
    git remote add origin https://github.com/YOUR-USERNAME/student-course-api.git
    git push -u origin main

---

## 7. Deploy to Render

1. Sign in at render.com with your GitHub account.
2. Click New + and choose Web Service.
3. Choose "Build and deploy from a Git repository" and connect
   student-course-api.
4. Fill in the settings:
   - Name: student-course-api
   - Language: Python 3
   - Region: the one closest to you
   - Branch: main
   - Root Directory: leave empty
   - Build Command: pip install -r requirements.txt
   - Start Command: gunicorn app:app
   - Instance Type: Free
5. Click Create Web Service and wait for the log to say the service is live.
6. Open https://YOUR-SERVICE-NAME.onrender.com/api/health in a browser.
   A JSON answer means the deployment worked.

Environment variables: none are needed. Render sets PORT itself, and app.py
reads it with os.environ.get("PORT", 5000).

---

## 8. Honest notes

- The data is stored in app.py, not in a database. Nothing is persisted or
  connected to any external database.
- There is no authentication, by design: the API is read-only and public.
- On Render's free tier the service sleeps after about fifteen minutes of
  inactivity, so the next request can take up to a minute to wake it up.
- The production server is Gunicorn through gunicorn app:app. The python app.py
  command is only for local development.
