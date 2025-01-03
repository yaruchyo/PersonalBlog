from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import db, bcrypt, file_storage
from flaskblog.service_layer.models import User, Post
from flaskblog.routes_layer.users.forms import (LoginForm, UpdateAccountForm)
from flaskblog.routes_layer.users.utils import save_profile_picture
import os

users = Blueprint('users', __name__)

admin_path = os.getenv("ADMIN_PATH")
@users.route(f"/{admin_path}", methods=['GET', 'POST'])
def admin():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user_data = db.find_document("users", {'username': form.username.data})
        if user_data and bcrypt.check_password_hash(user_data['password'], form.password.data):
            user = User(user_data)
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            #delete_picture('static/profile_pics', current_user.image_file)
            picture_file = save_profile_picture(form.picture.data)
            current_user.image_file = picture_file
        if form.password.data:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            current_user.password = hashed_password
        current_user.legal_name = form.legal_name.data
        current_user.username = form.username.data
        current_user.email = form.email.data
        User.update_user_data(current_user)
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.legal_name.data = current_user.legal_name
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


# @users.route("/user/<string:username>")
# def user_posts(username):
#     page = request.args.get('page', 1, type=int)
#     user = User.query.filter_by(username=username).first_or_404()
#     posts = Post.query.filter_by(author=user)\
#         .order_by(Post.date_posted.desc())\
#         .paginate(page=page, per_page=5)
#     return render_template('user_posts.html', posts=posts, user=user)


