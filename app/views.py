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
    form = MovieForm()
    errors = []
    status_code = 201
    basedir = os.path.abspath(os.path.dirname(__file__))
    print(basedir)
    if request.method == "POST":
        try:
            if form.validate_on_submit():
                if form_errors(form) != []: 
                    errors = form_errors(form)
                    status_code = 400
                    return jsonify({"errors": errors}), status_code
              
                poster_file = form.poster.data
              
                poster_filename = secure_filename(poster_file.filename)
                
                basedir = os.path.abspath(os.path.dirname(__file__))
                print(basedir)

                poster_path = os.path.join(basedir, app.config['UPLOAD_FOLDER'], poster_filename)
                poster_file.save(poster_path)
                
                movie = Movie(
                    title=form.title.data, 
                    poster=poster_path, 
                    description=form.description.data
                )
                db.session.add(movie)
                db.session.commit()
          
                if movie.id is None:
                    status_code = 500
                    return jsonify({"error": "Failed to save movie to the database"}), status_code
                
                return jsonify({
                    "id": movie.id,
                    "title": movie.title,
                    "poster": movie.poster,
                    "description": movie.description,
                    "message": "Movie successfully added to the database"
                }), status_code
            
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    return render_template('movie-form.html', form=form)


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