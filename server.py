"""Glitzy"""
import os
import hashlib
import datetime

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session, url_for
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Login, Glitz, Grid, Comment

from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'glitz'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'img'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


def encrypt_password(password):
    # encrypt password sent by user 
    h = hashlib.md5(password.encode())
    encrypted_password = h.hexdigest()
    
    return encrypted_password    


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")


@app.route('/register', methods=['GET'])
def register_form():
    """Show form for user signup."""

    return render_template("register_form.html")


@app.route('/register', methods=['POST'])
def register_process():
    """Process registration."""

    # Get form variables
    lname = request.form["lname"]
    fname = request.form["fname"]
    email = request.form["email"]
    password = request.form["password"]
    
    new_user = User(fname=fname, lname=lname)

    db.session.add(new_user)
    db.session.commit()
    
    new_password = encrypt_password(password)

    new_login = Login(user_id=new_user.user_id, email=email, password=new_password)

    db.session.add(new_login)
    db.session.commit()



    # flash("User %s added." % email)
    return redirect("/%s" % new_user.user_id)


@app.route("/<int:user_id>")
def user_detail(user_id):
    """Show info about user."""

    user = User.query.options(db.joinedload('logins')).get(user_id)
    return render_template("homepage.html", user=user)



@app.route('/login', methods=['GET'])
def login_form():
    """Show login form."""

    return render_template("login_form.html")


@app.route('/login', methods=['POST'])
def login_process():
    """Process login."""

    # Get form variables
    email = request.form["email"]
    password = request.form["password"]

    encrypted_password = encrypt_password(password)

    logged_in_user = Login.query.filter_by(email=email).first()

    if not logged_in_user:
        flash("No such user")
        return redirect("/login")

    if logged_in_user.password != encrypted_password:
        flash("Incorrect password")
        return redirect("/login")

    session["user_id"] = logged_in_user.user_id

    flash("Logged in")
    # return redirect("/")
    return redirect("/%s" % logged_in_user.user_id)


@app.route('/logout')
def logout():
    """Log out."""

    del session["user_id"]
    flash("Logged Out.")
    return redirect("/")

"""
Check for specific allowed file extensions
"""
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_glitz_data(path, user_id, title):
    # Save glitz to DB
    now = datetime.datetime.now()
    glitz = Glitz(glitz_path=path, user_id=user_id, posted_on=now, title=title)

    db.session.add(glitz)
    db.session.commit()



@app.route('/upload_glitz', methods=['POST'])
def upload_glitz():
    """Upload Glitz."""

    # Get image 
    if request.method == 'POST':
        # check if the post request has the file part
        
        if 'glitzToUpload' not in request.files:
            # flash('No file part')
            return redirect("/")

        file = request.files['glitzToUpload']

        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            # flash('No selected file')
            return redirect("/")

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            
            # Save file to disk
            path_to_save_file = os.path.join(app.config['UPLOAD_FOLDER'], 
                filename)
            file.save(path_to_save_file)

            # Save to DB
            save_glitz_data(path=path_to_save_file, user_id=session["user_id"], 
                title='yeah!')
            # upload.save(path_to_save_file)

            # return redirect("homepage.html", image_name=filename)

            return redirect("/")

    return redirect("/")


# @app.route('/show/<filename>')
# def uploaded_glitz(filename):
#     filename = 'http://127.0.0.1:5000/uploads/' + filename
#     return render_template('/', filename=filename)


# @app.route('/uploads/<filename>')
# def send_glitz(filename):
#     return send_from_directory(UPLOAD_FOLDER, filename)



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension

    # Do not debug for demo
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
