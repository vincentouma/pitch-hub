from . import db 
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    pass_secure = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True, index=True)
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    password_hash = db.Column(db.String(255))
    pitches = db.relationship("Pitches", backref="user", lazy="dynamic")
    comment = db.relationship("Comments", backref="user", lazy="dynamic")

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.pass_secure, password)

    def __repr__(self):
        return f'User {self.username}'


class PitchListing(db.Model):
    '''
    Listing class define listing per pitch
    '''
    __tablename__ = 'pitch_listing'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.String(255))

    # save pitches
    def save_listing(self):
        '''
        Function that saves a listing
        '''
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_listing(cls):
        '''
        Function that returns all the data from the listing after being queried
        '''
        listing = PitchListing.query.all()
        return listing

class Pitches(db.Model):

    """
    Class that holds instances of all the pitches in the different listing
    """
    all_pitches = []

    __tablename__ = 'pitches'

    id = db.Column(db.Integer, primary_key=True)
    actual_pitch = db.Column(db.String)
    date_posted = db.Column(db.DateTime, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    listing = db.Column(db.String(200))
    comment = db.relationship("Comments", backref="pitches", lazy="dynamic")


    def save_pitch(self):
        '''
        Function to save a pitch
        '''
        db.session.add(self)
        db.session.commit()

    @classmethod
    def clear_pitches(cls):
        """Function which clears all the pitches in a particular listing"""
        Pitches.all_pitches.clear()
 
    # display pitches
    @classmethod
    def get_pitches(cls, id):
        """Function which gets a particular pitch when requested by date posted"""
        pitches = Pitches.query.order_by(Pitches.date_posted.desc()).filter_by(listing_id=id).all()
        return pitches



class Comments(db.Model):
    '''
    Comment class that creates instances of Comments class that will be attached to a particular pitch
    '''
    __tablename__ = 'comment'

    # add columns
    id = db.Column(db. Integer, primary_key=True)
    actual_comment = db.Column(db.String)
    comment_id = db.Column(db.String(255))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    pitches_id = db.Column(db.Integer, db.ForeignKey("pitches.id"))


    def save_comment(self):
        '''
        Save the comments per pitch
        '''
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(self, id):
        comment = Comments.query.order_by(
            Comments.date_posted.desc()).filter_by(pitches_id=id).all()
        