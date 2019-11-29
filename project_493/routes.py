import html
import secrets
import os

from PIL import Image
from flask import render_template, flash, redirect, url_for, request, abort
from project_493.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from project_493.models import User, Post
from project_493 import app, db, bcpt
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
@app.route("/home")
def home() -> html:
    page = request.args.get('page', 1, type=int)
    posts = Post.query.paginate(page=page, per_page=10)
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


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post() -> html:
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post', form=form, legend="New post")


@app.route("/post/<int:post_id>")
def post(post_id) -> html:
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id) -> html:
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:  # Something we can take away and do an attack on
        abort(403)

    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('The post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))

    elif request.method == 'GET':
        form = PostForm()
        form.title.data = post.title
        form.content.data = post.content

    return render_template('create_post.html', title='Update post', form=form, legend="Update post")


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id) -> html:
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:  # Something we can take away and do an attack on
        abort(403)

    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))