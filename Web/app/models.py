from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager

class Users(UserMixin, db.Model):

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    password_hash = db.Column(db.String(128)) 


    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('Password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User: {}>'.format(self.username)

class Camera(UserMixin, db.Model):
    
    __tablename__ = 'camera'
   
    cno = db.Column(db.String(60), nullable = False, unique=True, primary_key = True)
    username = db.Column(db.String(60), db.ForeignKey("users.username", ondelete='CASCADE'))
    cdesc = db.Column(db.String(120) , nullable = False)

    def __repr(self):
        return '<Camera :{}>'.format(self.username)

class Profile(UserMixin, db.Model):
        
    __tablename__ = 'profile'

    #id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(60), db.ForeignKey("users.username", ondelete='CASCADE'), nullable = False, unique=True, primary_key = True)
    first_name = db.Column(db.String(120) , nullable = False)
    last_name = db.Column(db.String(120) , nullable = True)

    def __repr(self):
        return '<Profile :{}>'.format(self.username)

class Persons(UserMixin, db.Model):
        
    __tablename__ = 'persons'

    person_id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(60), db.ForeignKey("users.username", ondelete='CASCADE'), nullable = False)
    person_name = db.Column(db.String(60), nullable = False)
    azure_id = db.Column(db.String(60), nullable = False)
    
    def __repr(self):
        return '<Persons :{}>'.format(self.username)

class AuthImageGallery(UserMixin, db.Model):
    __tablename__= 'authImageGallery'
    imgid = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey("persons.person_id", ondelete='CASCADE'), nullable = False)
    image_filename = db.Column(db.String(60), default= None, nullable= False)
    image_path = db.Column(db.Text, default= None, nullable = False)
    training_status = db.Column(db.Text, nullable = False )

    def __repr(self):
        return '<AuthImageGallery :{}>'.format(self.username)

class UnauthImageGallery(UserMixin, db.Model):
    __tablename__= 'unauthImageGallery'

    imgid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), db.ForeignKey("users.username", ondelete='CASCADE'), nullable = True , unique = False)
    image_filename = db.Column(db.String(60), default= None, nullable= False)
    image_path = db.Column(db.Text, default= None, nullable = False)
    timestamp = db.Column(db.Text, nullable = False)
   # cameraID = db.Column(db.Text, nullable = False)

    def __repr(self):
        return '<UnauthImageGallery :{}>'.format(self.username)


@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))
