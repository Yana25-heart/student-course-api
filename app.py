"""
STUDENT COURSE API
Laboratory Activity 3A - Creating a Backend API

A small, read-only REST API built with Python and Flask. It serves six
fictional course records that live in this very file. There is no database,
no login, and no way to create, update or delete anything: only GET.

Run locally:        python app.py
Run in production:  gunicorn app:app
"""

import os

from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)

# CORS is opened up for the classroom demonstration so that a browser page,
# Postman, or a classmate's front end can call the API from any origin.
# A real production API would list its allowed origins explicitly here.
CORS(app, resources={r"/api/*": {"origins": "*"}})


# ---------------------------------------------------------------------------
# SAMPLE DATA
# Fictional courses only. No real student information is stored or served.
# In a bigger system this list would be replaced by a database query, but for
# this laboratory the data lives in the source code on purpose.
# ---------------------------------------------------------------------------
COURSES = [
    {
        "id": 1,
        "code": "IT-301",
        "name": "Systems Integration and Architecture",
        "description": "Integration patterns, middleware and messaging used to connect independent systems into one enterprise solution.",
    },
    {
        "id": 2,
        "code": "CS-204",
        "name": "Data Structures and Algorithms",
        "description": "Lists, stacks, queues, trees and graphs, plus the sorting and searching techniques that operate on them.",
    },
    {
        "id": 3,
        "code": "IT-215",
        "name": "Database Management Systems",
        "description": "Relational modelling, SQL, normalisation, transactions and indexing for reliable data storage.",
    },
    {
        "id": 4,
        "code": "CS-310",
        "name": "Web Systems and Technologies",
        "description": "The HTTP request-response cycle, REST resource design and the client-server model behind web services.",
    },
    {
        "id": 5,
        "code": "IT-402",
        "name": "Cloud Computing and Deployment",
        "description": "Virtual machines, containers, CI/CD pipelines and publishing a service to a cloud platform.",
    },
    {
        "id": 6,
        "code": "IT-330",
        "name": "Network Administration",
        "description": "Addressing, routing, switching and the monitoring tools used to keep a small network healthy.",
    },
]


def find_course(course_id):
    """Return the course with this id, or None when it does not exist."""
    for course in COURSES:
        if course["id"] == course_id:
            return course
    return None


# ---------------------------------------------------------------------------
# ENDPOINTS
# ---------------------------------------------------------------------------


@app.get("/api/health")
def health_check():
    """GET /api/health - proves the service is running."""
    return jsonify({"status": "success", "message": "Student Course API is running"}), 200


@app.get("/api/courses")
def get_courses():
    """GET /api/courses - the whole catalogue, as a JSON array."""
    return jsonify(COURSES), 200


@app.get("/api/courses/<int:course_id>")
def get_course(course_id):
    """GET /api/courses/<id> - one course, or a helpful 404."""
    course = find_course(course_id)
    if course is None:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "Course with id " + str(course_id) + " was not found.",
                    "available_ids": [item["id"] for item in COURSES],
                }
            ),
            404,
        )
    return jsonify(course), 200


# ---------------------------------------------------------------------------
# ERROR HANDLING
# Always answer with JSON, never with Flask's default HTML error page.
# ---------------------------------------------------------------------------


@app.errorhandler(404)
def handle_not_found(error):
    """Unknown URL."""
    return (
        jsonify(
            {
                "status": "error",
                "message": "That endpoint does not exist. Try GET /api/health, GET /api/courses or GET /api/courses/<id>.",
            }
        ),
        404,
    )


@app.errorhandler(405)
def handle_method_not_allowed(error):
    """The API is read-only, so anything except GET is refused."""
    return (
        jsonify(
            {
                "status": "error",
                "message": "This API is read-only. Only GET requests are allowed.",
            }
        ),
        405,
    )


if __name__ == "__main__":
    # Render hands the port to the app through the PORT environment variable.
    # Locally that variable is unset, so the app falls back to 5000.
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
