"""Models and database functions for Glitzy project."""

from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database; we're getting
# this through the Flask-SQLAlchemy helper library. On this, we can
# find the `session` object, where we do most of our interactions
# (like committing, etc.)

db = SQLAlchemy()


#####################################################################
# Model definitions

class User(db.Model):
    """User of Glitzy website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    fname = db.Column(db.String(25), nullable=False)
    lname = db.Column(db.String(25), nullable=False)


    def __repr__(self):
        """Provide helpful representation when printed."""

        return "\n<User ID: {} Name: {} {}>\n".format (self.user_id,
                                               self.fname,
                                               self.lname)


class Login(db.Model):
    """User of Glitzy website."""

    __tablename__ = "logins"

    login_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    user_id = db.Column(db.Integer,
                         db.ForeignKey('users.user_id'),
                         nullable=False)
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=True)

# Define relationship to grid
    user = db.relationship("User", backref="logins")


def __repr__(self):
        """Provide helpful representation when printed."""

        return "\n Login session - User ID: {} Email: {}\n".format(self.user_id,
                                                 self.email)


class Glitz(db.Model):
    """Glitz (image) on Glitzy website"""

    __tablename__ = "glitzes"

    glitz_id = db.Column(db.Integer,
                         autoincrement=True,
                         primary_key=True)
    user_id = db.Column(db.Integer,
                         db.ForeignKey('users.user_id'),
                         nullable=False)
    title = db.Column(db.String(250))
    posted_on = db.Column(db.DateTime, nullable=False)
    glitz_path = db.Column(db.String(250), nullable=False)

    # Define relationship to grid
    user = db.relationship("User", backref="glitzes")


    def __repr__(self):
        """Provide helpful representation when printed."""

        return "\n Glitz ID: {} Title: {}\n".format(self.glitz_id,
                                                 self.title)


class Grid(db.Model):
    """Grid at Glitz (image) on glitzy website"""

    __tablename__ = "grids"

    grid_id = db.Column(db.Integer,
                         autoincrement=True,
                         primary_key=True)
    grid_name = db.Column(db.String(25), nullable=False)
    
    def __repr__(self):
        """Provide helpful representation when printed."""

        return "\n<Grid ID: {}  Name: {}>".format(self.grid_id,
                                                      self.grid_name)


class Comment(db.Model):
    """Comments on Glitz by a user on Glitzy website."""

    __tablename__ = "comments"

    comment_id = db.Column(db.Integer,
                          autoincrement=True,
                          primary_key=True)
    glitz_id = db.Column(db.Integer,
                         db.ForeignKey('glitzes.glitz_id'), 
                         nullable=False)
    grid_id = db.Column(db.Integer, db.ForeignKey('grids.grid_id'), 
                        nullable=False)
    comment_text = db.Column(db.Text, nullable=False)
    commented_on = db.Column(db.DateTime, nullable=False)

    # Define relationship to glitz
    glitz = db.relationship("Glitz",
                           backref=db.backref("comments",
                                              order_by=comment_id))

    # Define relationship to grid
    grid = db.relationship("Grid", backref="comments")


    def __repr__(self):
        """Provide helpful representation when printed."""

        return "\n<Comment ID: {}  Title: {}>".format(self.comment_id,
                                                      self.title)


#####################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///glitzy'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will
    # leave you in a state of being able to work with the database
    # directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
    db.create_all()