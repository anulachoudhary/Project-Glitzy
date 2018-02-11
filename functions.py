import hashlib
import datetime

from model import connect_to_db, db, User, Login, Glitz, Grid, Comment

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'img'])

"""
Encrypt password
"""
def encrypt_password(password):
    # encrypt password sent by user 
    h = hashlib.md5(password.encode())
    encrypted_password = h.hexdigest()
    
    return encrypted_password    


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

    return glitz.glitz_id


def save_comment_data(glitz_id, user_id, grid_id, comment_text):
    # save to DB
    now = datetime.datetime.now()

    comment = Comment(glitz_id=glitz_id, user_id=user_id, grid_id=grid_id, 
                      commented_on=now, comment_text=comment_text)

    db.session.add(comment)
    db.session.commit()

    return comment.comment_id
