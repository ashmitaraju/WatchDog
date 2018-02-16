from app import app
from flask import render_template, redirect, flash, url_for, request, make_response
from flask_login import login_required, login_user, logout_user, current_user
from .forms import *
from app import db, images
from .models import *
import datetime
from werkzeug.utils import secure_filename
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .camera import *


@app.route('/', methods = ['GET', 'POST']) 
def homepage():
  return render_template('index.html', title = 'Home') 

@app.route('/index')
def index():
    return render_template('index.html', title = 'Home')

@app.route('/signup', methods=['GET','POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        user = Users(email=form.email.data, username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash('Registration Successful! You may now create your profile.')
        return redirect(url_for('editProfile'))
    return render_template('signup.html', title='Sign Up', form = form)

@app.route('/login' , methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('cameraDetails'))

    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email = form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)

            return redirect(url_for('dashboard')) 
        else:
            flash('Invalid email or password', 'danger')
    return render_template('login.html', title='Sign In', form = form)

@app.route('/editProfile', methods=['GET', 'POST'])
@login_required
def editProfile():
    profile = Profile.query.filter_by(username = current_user.username).first()
    if profile is None:
        form = EditProfileForm() 
        if form.validate_on_submit():
            profile = Profile(username = current_user.username, first_name = form.first_name.data, last_name = form.last_name.data)
            print profile 
            db.session.add(profile)
            db.session.commit()
            return redirect(url_for('cameraDetails'))
    else: 
        form = EditProfileForm(obj=profile)
        form.populate_obj(profile)
        if form.validate_on_submit():
            print "hey"
            profile = Profile(username = current_user.username, first_name = form.first_name, last_name = form.last_name)
            print profile 
            db.session.commit()
            return redirect(url_for('cameraDetails'))
    return render_template('editProfile.html', title='Edit Profile', form = form)


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    profile = Profile.query.filter_by(username = current_user.username).first()
    return render_template('dashboard.html' ,  profile = profile)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have logged out.')
    return redirect(url_for('login' ))

@app.route('/cameraDetails' , methods = ['GET' , 'POST'])
@login_required
def cameraDetails():
    camera = Camera.query.filter_by(username = current_user.username).all()
    if request.method == 'POST':
        if request.form['submit'] == 'Submit':    
            detailsList = request.form.getlist('myInputs[]')
            CameraNoList = detailsList[0::2]
            CameraDescList = detailsList[1::2] 
            length = len(CameraNoList)
            for i in range(0,length):
                camera = Camera(username = current_user.username , cno = CameraNoList[i] , cdesc = CameraDescList[i])
                db.session.add(camera)
                db.session.commit()
            return redirect(url_for('dashboard'))
    return render_template('cameraDetails.html' , camera = camera)


@app.route('/unAuth' , methods = ['GET' , 'POST'])
@login_required
def unAuth():
    form = EditImageGalleryForm()
    return render_template('Auth.html', form = form)

@app.route('/train' , methods = ['GET' , 'POST'])
@login_required
def train():
    return 'Hello World' 
    

@app.route('/uploadImages', methods=['GET', 'POST'])
@login_required
def uploadImages():
    count = 0
    pics = []
    x = db.session.query(Persons.person_name,AuthImageGallery.image_path).filter(Persons.person_id == AuthImageGallery.person_id, Persons.username == current_user.username).all()
    print x
    form = EditImageGalleryForm()

    if form.picture.data: 
        print "picture"
        person = Persons(person_name = form.name.data, username = current_user.username)
        db.session.add(person)
        db.session.commit()
        naam = form.name.data
        takePicture(naam)

    if form.submit.data or form.skip.data: 
        print "hello"
        person = Persons(person_name = form.name.data, username = current_user.username)
        db.session.add(person)
        db.session.commit()   
        if 'image' in request.files:

            for f in request.files.getlist('image'):
                print f
                if f.filename:
                    print "hi"
                    filename = secure_filename(f.filename)
                    f.save(os.path.join(app.config['UPLOADED_IMAGES_DEST'], filename))
                    url = "../static/img/" + filename
                    person = Persons.query.filter_by(person_name = form.name.data).first()
                    image = AuthImageGallery(image_filename= filename, image_path= url, person_id = person.person_id )
                    db.session.add(image)
                    db.session.commit()
                    print "done"
            if form.submit.data:
                return redirect(url_for('uploadImages'))
            if form.skip.data:
                return redirect(url_for('dashboard'))
                    
    return render_template('Auth.html' , form = form, x = x)

@app.route('/deleteImages', methods=['GET', 'POST'])
@login_required
def deleteImages():
    pics = db.session.query(Persons.person_name,AuthImageGallery.imgid , AuthImageGallery.image_filename,AuthImageGallery.image_path).filter(Persons.person_id == AuthImageGallery.person_id, Persons.username == current_user.username).all()
    print pics
    delPics = []
    if request.method == "POST":
        delPics = request.form.getlist('users')
    print delPics 
    if delPics:
        for f in delPics:
            print f
            img = AuthImageGallery.query.filter_by(imgid = f).first()
            os.remove(os.path.join(app.config['UPLOADED_IMAGES_DEST'], img.image_filename))
            db.session.delete(img)
            db.session.commit()
        return redirect(url_for('uploadImages'))
    return render_template('deleteImages.html' , pics = pics)