import html
import secrets
import os

from PIL import Image
from flask import render_template, flash, redirect, url_for, request
from project_493.forms import RegistrationForm, LoginForm, UpdateAccountForm
from project_493.models import User, Post
from project_493 import app, db, bcpt
from flask_login import login_user, current_user, logout_user, login_required

# Temp posts
posts = [
    {
        "account" :"McKade Sorensen",
        "tweet" : "@ChenyiLing How are you doing?",
        "date_posted" : "10/5/2019"
    },
    {
        "account" :"Chenyi Ling",
        "tweet" : "@McKadeSorensen Great",
        "date_posted" : "10/6/2019"
    }
]


@app.route("/")
@app.route("/home")
def home() -> html:
    return render_template('home.html', posts=posts)


@app.route("/about")
def about() -> html:
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register() -> html:

    if current_user.is_authenticated:
         return redirect(url_for('home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pswd = bcpt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pswd)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created! You can now login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title="Register", form=form)


@app.route("/login", methods=['GET', 'POST'])
def login() -> html:

    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and bcpt.check_password_hash(user.password, form.password.data):  # Hashed password
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Check email and password.', 'danger')

    return render_template('login.html', title="Login", form=form)


@app.route("/logout")
def logout() -> html:
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture) -> str:
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_file_name = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_file_name)

    # Resize image to save space on file system
    output_size = (125, 125)
    img = Image.open(form_picture)
    img.thumbnail(output_size)
    img.save(picture_path)

    return picture_file_name


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account() -> html:
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_path = save_picture(form.picture.data)
            current_user.image_file = picture_path
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your CatBook has been updated!', 'success')
        return redirect(url_for('account'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)