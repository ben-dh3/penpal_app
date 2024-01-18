"""
views imports app, auth, and models, but none of these import views
"""
from flask import Flask, session, request, render_template, redirect
from datetime import datetime
from app import app
from models import User, Post

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
    message = request.form['message']
    t = datetime.now()
    time = t.strftime("%H:%M:%S")
    try:
        Post.create(message=message, time=time, sender_id=sender_id, recipient_id=recipient_id)
        return render_template('users/signup_success.html')
    except:    
        return "account exists"


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
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    nationality = request.form['nationality']  
    try:
        User.create(name=name, email=email, password=password, nationality=nationality)
        return render_template('users/signup_success.html')
    except:    
        return "account exists"
