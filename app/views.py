"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from app import app
from flask import render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
from flask_wtf.csrf import generate_csrf
from app.forms import MovieForm
from app.models import Movie
from app.utils import get_uploaded_images
from . import db


###
# Routing for your application.
###

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")

@app.route("/api/v1/csrf-token", methods=["GET"])
def get_csrf():
    return jsonify({"csrf_token": generate_csrf()})

@app.route("/api/v1/movies", methods=["GET", "POST"])
def movies():
    errors = []
    if request.method == "GET":
        movies = Movie.query.all()
        movies_list = [{"id": movie.id, "title": movie.title, "poster": movie.poster, "description": movie.description} for movie in movies]
        return jsonify(movies_list), 200

    if request.method == "POST":
        form = MovieForm()

        if not form.validate_on_submit():
            errors = form_errors(form)
            return jsonify({"errors": errors}), 400

        missingErrors = []
        if form.title.data == "":
            missingErrors.append("Error in the 'Title' field: Title is required.")
        if form.description.data == "":
            missingErrors.append("Error in the 'Description' field: Description is required.")
        if form.poster.data is None:
            missingErrors.append("Error in the 'Poster' field: Poster is required.")

        if len(missingErrors) > 0:
            return jsonify({"errors": missingErrors}), 400

        try:
         
            poster_file = form.poster.data
            poster_filename = secure_filename(poster_file.filename)
            poster_path = os.path.join(app.config['UPLOAD_FOLDER'], poster_filename)
            
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        
            poster_file.save(poster_path)

            movie = Movie(title=form.title.data, poster=poster_path, description=form.description.data)
            db.session.add(movie)
            db.session.commit()
            
            return jsonify({
            "id": movie.id,
            "title": movie.title,
            "poster": movie.poster,
            "description": movie.description,
            "message": "Movie successfully added to the database"
        }), 201
            
        except Exception as e:
            return jsonify({"errors": e}), 400
            
       

        

###
# The functions below should be applicable to all Flask apps.
###

# Here we define a function to collect form errors from Flask-WTF
# which we can later use
def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404