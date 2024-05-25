import threading

# import "packages" from flask
from flask import render_template,request, jsonify  # import render_template from "public" flask libraries
from flask.cli import AppGroup

# import "packages" from "this" project
from __init__ import app, db, login_manager #cors  # Definitions initialization

# Import necessary modules from the project
from flask import redirect, render_template, request, url_for  # import render_template from "public" flask libraries
from flask_login import login_user, logout_user
from __init__ import app, db
from api.user import user_api
from api.titanic import titanic_api
from api.depression import predict_api
from api.stroke import stroke_api
from api.heart import heart_api
from api.therapy import therapy_api
from api.hotline import hotline_api
from api.recipe import recipe_api
from api.qtee import qt1_api
from api.quote import quote_api
from api.kpopapi import kpop_api
from model.users import initUsers, User
from model.titanic import initTitanic
from model.heart import initHeart
from model.strokes import initStroke
from model.depression import initDepression
from model.therapies import initTherapies
from model.recipes import initRecipes
from model.quotes import initQuotes
from model.qtees import initqt1s
from model.hotlines import initHotlines
from projects.projects import app_projects

# Initialize the SQLAlchemy object to work with the Flask app instance
db.init_app(app)

#class Quote(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    quote_text = db.Column(db.String(255), nullable=False)
#    quote_author = db.Column(db.String(100), nullable=False)
#    user_opinion = db.Column(db.Text, nullable=False)


# Register URIs
app.register_blueprint(user_api)
app.register_blueprint(titanic_api)
app.register_blueprint(stroke_api)
app.register_blueprint(heart_api)
app.register_blueprint(predict_api)
app.register_blueprint(therapy_api)
app.register_blueprint(hotline_api)
app.register_blueprint(quote_api)
app.register_blueprint(qt1_api)
app.register_blueprint(recipe_api)
app.register_blueprint(app_projects)
app.register_blueprint(kpop_api)


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(_uid=user_id).first()

@app.errorhandler(404)  # catch for URL not found
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

@app.route('/')  # connects default URL to index() function
def index():
    return render_template("index.html")

@app.route('/table/')  # connects /stub/ URL to stub() function
def table():
    return render_template("table.html")

@app.route('/login/')  # connects /table/ URL
def login_page():
    return render_template("login.html")

@app.route('/login', methods=['POST'])
def login():
    # authenticate user
    user = User.query.filter_by(username=request.form['username']).first()
    if user and user.check_password(request.form['password']):
        login_user(user)
        return redirect(url_for('index'))
    else:
        return 'Invalid username or password'

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))




@app.route('/api/users/save_settings', methods=['POST'])  # Define the route for saving settings
def save_settings():
    try:
        # Extract settings data from the request
        settings = request.json.get('settings')

        # Update the user's settings in the database (replace 'current_user' with your actual user object)
        # Example: current_user.update_settings(settings)
        # Make sure to implement this method in your User model

        return jsonify({'message': 'Settings saved successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

        
# Create an AppGroup for custom commands
custom_cli = AppGroup('custom', help='Custom commands')

# Define a command to generate data
@custom_cli.command('generate_data')
def generate_data():
    initUsers()
    initTherapies()
    initTitanic()
    initStroke()
    initHeart()
    initDepression()
    initRecipes()
    initQuotes()
    initHotlines()
    initqt1s()


# Register the custom command group with the Flask application
app.cli.add_command(custom_cli)

# Run the application on the development server
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, host="0.0.0.0", port="8432")