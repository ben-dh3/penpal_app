"""
views imports app, auth, and models, but none of these import views
"""
import os
from flask import Flask, session, request, render_template, redirect
from datetime import datetime
from werkzeug.utils import secure_filename
from app import app, sanitizer, ALLOWED_EXTENSIONS
from models import User, Post
import re

def allowed_file(filename):
    check = str(filename).split('.')[1]
    return check.split("'")[0].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def get_users():
    if not session.get("user_id"):
        return redirect('/login')
    user_id = session.get("user_id")
    users = User.select().where(User.id != user_id)
    return render_template('users/index.html', users=users)


@app.route("/", methods=['POST'])
def penpal_post():
    user_id = session.get("user_id")
    # find recipient
    recipient_name = request.form['name']
    recipient_id = User.get(User.name == recipient_name).id
    sender_id = User.get(User.id == user_id).id
    message = sanitizer.sanitize(request.form.get('message'))
    t = datetime.now()
    time = t.strftime("%H:%M:%S")
    try:
        Post.create(message=message, time=time, sender_id=sender_id, recipient_id=recipient_id)
        return "Message sent"
    except:    
        return "Message failed"


# This route simply returns the login page
@app.route('/login')
def login():
    if not session.get("user_id"):
        return render_template('users/login.html')
    return redirect('/')

@app.route('/login', methods=['POST'])
def login_post():
    email = request.form['email']
    password = request.form['password']   
    user_id = User.get((User.email == email) & (User.password == password)).id
    # Set the user ID in session
    session['user_id'] = user_id
    return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


# This route simply returns the signup page
@app.route('/signup')
def signup():
    if not session.get("user_id"):
        return render_template('users/signup.html')
    else:
        return redirect('/')


@app.route('/signup', methods=['POST'])
def signup_post():
    name = sanitizer.sanitize(request.form.get('name'))
    email = request.form['email']
    password = request.form['password']
    nationality = request.form['nationality']
    profile_picture = request.files['profile_picture']
    # secure file
    if allowed_file(profile_picture):
            profile_picture.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(profile_picture.filename)))
            print("here")
    else:
        return "no"
    # name must be unique
    try:
        User.get(User.name == name)
        return render_template('users/username_not_unique.html')
    except:
    # check email and password are valid
        if email is None or password is None or name is None or nationality is None:
            return render_template('users/signup_error.html')
        if re.match(r"^\S+@\S+\.\S+$", email, re.I) and re.match(r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$", password):
            try:
                User.create(name=name, email=email, password=password, nationality=nationality, profile_picture=secure_filename(profile_picture.filename))
                return render_template('users/signup_success.html')
            except:    
                return "Email associated with another account"
        else:
            return render_template('users/signup_error.html')
        
