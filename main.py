import threading

# Import necessary packages from flask
from flask import render_template, request, jsonify
from flask.cli import AppGroup
from flask_cors import CORS

# Import necessary modules from the project
from __init__ import app, db
from api.user import user_api
from api.titanic import titanic_api
from api.depression import predict_api
from api.stroke import stroke_api
from api.heart import heart_api
from api.activity import activity_api
from model.users import initUsers
from model.titanic import initTitanic
from model.heart import initHeart
from model.strokes import initStroke
from model.depression import initDepression
from model.activities import initActivities
from projects.projects import app_projects

# Initialize the SQLAlchemy object to work with the Flask app instance
db.init_app(app)

class Quote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quote_text = db.Column(db.String(255), nullable=False)
    quote_author = db.Column(db.String(100), nullable=False)
    user_opinion = db.Column(db.Text, nullable=False)

# Register URIs
app.register_blueprint(user_api)
app.register_blueprint(titanic_api)
app.register_blueprint(stroke_api)
app.register_blueprint(heart_api)
app.register_blueprint(predict_api)
app.register_blueprint(activity_api)
app.register_blueprint(app_projects)

# Initialize CORS
CORS(app)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/table/')
def table():
    return render_template("table.html")

# Manually handle CORS headers for the quote-repository route
@app.route('/quote-repository', methods=['GET', 'POST', 'OPTIONS'])
def quote_repository():
    if request.method == 'OPTIONS':
        # Handle preflight request
        response = app.make_default_options_response()
    elif request.method == 'GET':
        # Handle GET request
        quotes = Quote.query.all()
        quotes_list = [{'quote_text': quote.quote_text, 'quote_author': quote.quote_author, 'user_opinion': quote.user_opinion} for quote in quotes]
        response = jsonify({'quotes': quotes_list})
    else:
        # Handle POST request
        data = request.get_json()
        new_quote = Quote(
            quote_text=data.get('quote'),
            quote_author=data.get('quote_author'),
            user_opinion=data.get('opinion')
        )
        db.session.add(new_quote)
        db.session.commit()
        response_data = {'message': 'Quote submitted successfully'}
        response = jsonify(response_data)

    # Set CORS headers
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'

    return response

# Create an AppGroup for custom commands
custom_cli = AppGroup('custom', help='Custom commands')

# Define a command to generate data
@custom_cli.command('generate_data')
def generate_data():
    initUsers()
    initActivities()
    initTitanic()
    initStroke()
    initHeart()
    initDepression()

# Register the custom command group with the Flask application
app.cli.add_command(custom_cli)

# Run the application on the development server
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, host="0.0.0.0", port="8086")