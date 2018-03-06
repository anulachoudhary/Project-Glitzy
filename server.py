"""Glitzy"""
import os
import pdb
import datetime
import json
from functions import * 
from response import *
from jinja2 import StrictUndefined
from flask import Flask, render_template, request, flash, jsonify, redirect, session, url_for
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, User, Login, Glitz, Grid, Comment
from werkzeug.utils import secure_filename
from sqlalchemy import func, desc
from sqlalchemy.orm import aliased


UPLOAD_FOLDER = 'glitz'

app = Flask(__name__, static_folder = "glitz")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.jinja_env.undefined = StrictUndefined
app.jinja_env.auto_reload = True


# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined
    

@app.route('/')
def index():
    """Profile page."""

    if not is_user_logged_in(session):
        return redirect("/login")

    glitz_feeds = (db.session.query
                                (Glitz.glitz_path
                                    ,Glitz.glitz_id
                                    ,func.count(Comment.comment_id)
                                    ,User.user_id
                                    ,(User.fname + ' ' + User.lname).label('name')
                                    ,Glitz.posted_on
                                    ,Login.email)
                                .outerjoin(User, User.user_id == Glitz.user_id)
                                .outerjoin(Comment, Comment.glitz_id == Glitz.glitz_id)
                                .outerjoin(Login, User.user_id == Login.user_id)
                                .group_by(Glitz.glitz_path
                                          ,Glitz.glitz_id
                                          ,User.user_id
                                          ,'name'
                                          ,Glitz.posted_on
                                          ,Login.email)
                                .order_by(desc(Glitz.posted_on))
                                .all())


    return render_template("profile.html", glitz_feeds=glitz_feeds
                           ,user_name=session.get("user_name", "User"))                                                   



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

    existing_email = db.session.query(Login.email).filter(Login.email == email).first()

    if existing_email is not None:
        response = Response(False, "", "Email already registered. Please login.")
        return jsonify(response.__dict__) 


    new_user = User(fname=fname, lname=lname)

    db.session.add(new_user)
    db.session.commit()
    
    new_password = encrypt_password(password)

    new_login = Login(user_id=new_user.user_id, email=email, password=new_password)

    db.session.add(new_login)
    db.session.commit()

    session["user_id"] = new_login.user_id
    session["user_name"] = fname 

    response = Response(True, "/")
    return jsonify(response.__dict__)




# @app.route("/<int:user_id>")
# def user_detail(user_id):
#     """Show info about user."""

#     user = User.query.options(db.joinedload('logins')).get(user_id)
#     return render_template("profile.html", user=user)



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
        response = Response(False, "", "User not found. Please register.")
        return jsonify(response.__dict__)

    if logged_in_user.password != encrypted_password:
        response = Response(False, "", "Wrong password, please try again!")
        return jsonify(response.__dict__)        


    session["user_id"] = logged_in_user.user_id
    logged_in_user_details = User.query.get(logged_in_user.user_id)

    session["user_name"] = logged_in_user_details.fname 

    response = Response(True, "/")
    return jsonify(response.__dict__)


@app.route('/logout')
def logout():
    """Log out."""

    del session["user_id"]
    return redirect("/")

@app.route('/upload_glitz', methods=['POST'])
def upload_glitz():
    """Upload Glitz."""

    if not is_user_logged_in(session):
            return redirect("/login")

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
            glitz_id = save_glitz_data(path=path_to_save_file, 
                                    user_id=session["user_id"], title='yeah!')

            return redirect("/view_glitz/" + str(glitz_id))
            # return render_templatew_glitz.html", file_path=path_to_save_file)

    return redirect("/")


# Make new route and new def for that route
@app.route('/view_glitz/<int:glitz_id>')
def view_glitz(glitz_id):
    
    if not is_user_logged_in(session):
        return redirect("/login")

    # Using glitz_id, we need to fetch glitz data from DB
    grids = Grid.query.all()

    # # Glitz_User = aliased(User)
    # Comments_User = aliased(User)

    # Get the glitz detail 
    glitz_details = (db.session.query
                        (Glitz.glitz_path
                            ,Glitz.glitz_id
                            ,User.user_id
                            ,(User.fname + ' ' + User.lname).label('name'))
                        .join(User, User.user_id == Glitz.user_id)
                        .filter(Glitz.glitz_id == glitz_id)
                        .first())

    # Get the comments details 
    glitz_comments = (db.session.query
                                (Comment.comment_text
                                    ,Comment.user_id
                                    ,User.fname
                                    ,Comment.commented_on
                                    ,Comment.grid_id)
                                .join(User, User.user_id == Comment.user_id)
                                .filter(Comment.glitz_id == glitz_id)
                                .order_by(Comment.commented_on)
                                .all())

    # glitz_feeds = (db.session.query
    #                             (Glitz.glitz_path
    #                                 ,Glitz.glitz_id
    #                                 ,Comment.comment_text
    #                                 ,User.user_id
    #                                 ,(User.fname + ' ' + User.lname).label('name')
    #                                 ,Glitz.posted_on
    #                                 ,Comments_User.fname)
    #                             .outerjoin(Comment, Comment.glitz_id == Glitz.glitz_id)
    #                             .join(User, User.user_id == Glitz.user_id)
    #                             .join(Comments_User, Comments_User.user_id == Comment.user_id)
    #                             .filter(Glitz.glitz_id == glitz_id)
    #                             .order_by(Comment.commented_on)
    #                             .all())

    # glitz_comments = get_glitz_comments(glitz_feeds)  

    return render_template("view_glitz.html", glitz_details=glitz_details, glitz_comments=glitz_comments
                            ,grids=grids)                                                   



@app.route('/save_comment', methods=['POST'])
def save_comment():

    if not is_user_logged_in(session):
        return redirect("/login")
    
    # Get user_id from session 
    user_id = session["user_id"]
    
    # Get form variables
    comment = request.form["comment"]
    grid_id = request.form["select_grids"]
    glitz_id = request.form["glitz_id"]

    # save the comment on db
    comment_id = save_comment_data(glitz_id, user_id, grid_id, comment)

    # Create a dictionary to hold data for new comment
    comment_data = {}
    comment_data["glitz_id"] = glitz_id
    comment_data["grid_id"] = grid_id
    comment_data["comment"] = comment
    comment_data["user_name"] = session["user_name"] 

    response = Response(True, comment_data)

    # We need to pass in glitz_id, grid_id and comment_text from HTML form

    return jsonify(response.__dict__)



@app.route('/view_comments/<int:glitz_id>', methods=['GET', 'POST'])
def view_comments(glitz_id):

    if not is_user_logged_in(session):
        return redirect("/login")

    grids = Grid.query.all()

    # This route is re-used for two scenarios to load view_comments.js
    # First scenario: when we view comments for first time from other page
    # Second scenario: when we select a dropdown for the grid_id and reload comments

    # pdb.set_trace()
    select_grid_id = 0
    select_grid_name = "all"
    
    # When we select a dropdown (POST form)
    if request.method == 'POST':
        select_grid_id = request.form["select_grids"]
        comments = Comment.query.filter_by(glitz_id=glitz_id, grid_id=select_grid_id).all()
        select_grid_row = Grid.query.get(select_grid_id)
        select_grid_name = select_grid_row.grid_name

    # When we load comments
    else:
        comments = Comment.query.filter_by(glitz_id=glitz_id).all()

    # This needs special render variables (because we send selected
    # grid id)   
    return render_template("view_comments.js", comments=comments, 
                            grids=grids, 
                            glitz_id=glitz_id, 
                            select_grid_id=select_grid_id, 
                            select_grid_name=select_grid_name)


@app.route('/test')
def test():
    return render_template("/testloginregister.html")


# @app.route('/delete_glitz')
# def delete_glitz():
#     if not is_user_logged_in(session):
#         return redirect("/login")

#     glitz = db.session.query.filter(Glitz.glitz_id == glitz_id=glitz_id).first()
#     db.session.delete(glitz_id)



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension

    # Do not debug for demo
    app.debug = False

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
 