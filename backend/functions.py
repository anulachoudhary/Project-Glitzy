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


"""
Check if user is logged in
"""

def is_user_logged_in(session):

    # (session.get('user_id') == None) ? return False : return True
    if session.get('user_id') == None:
        return False
    else:
        return True


def get_glitz_comments(glitz_feeds):

    """
        {glitz_id:(glitz_path, user_id, name, posted_on, [(comment1, comment_author), (comment2, comment_author),..'])}
    """
    # Declare an emptry dictionary
    glitz_comments = {}
        
    for glitz_feed in glitz_feeds:
        feed_tuple = glitz_comments.get(glitz_feed.glitz_id)

        # First entry in dictionary
        if feed_tuple == None:
            # We do not want to put a null when comments dont exist 
            comments_list = []
            if glitz_feed.comment_text != None:
                comments_list.append((glitz_feed.comment_text, glitz_feed.fname))

            # Create tuple
            glitz_comments[glitz_feed.glitz_id] = (glitz_feed.glitz_path
                                                    ,glitz_feed.user_id
                                                    ,glitz_feed.name
                                                    ,comments_list
                                                    ,glitz_feed.posted_on)
        # Comments exist, now add more
        else:
            feed_tuple[3].append((glitz_feed.comment_text, glitz_feed.fname))
              
    # Can't use order_by in the query to sort as dictionary is immutable. 
    # Hence, use lambda to sort. 
    glitz_comments = sorted(glitz_comments.items(), key=lambda tup: tup[1][4], reverse=True)

    return glitz_comments

