
import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flaskblog import mail


def save_profile_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)
    i = Image.open(form_picture)
    w,h = i.size
    smaller_size = w if w < h else h
    crop_area = (0,0,smaller_size,smaller_size)
    i = i.crop(crop_area)
    output_size = (125, 125)
    i.thumbnail(output_size, Image.ANTIALIAS)
    i.save(picture_path)
    return picture_fn


def save_blog_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/post_pics', picture_fn)
    i = Image.open(form_picture)
    i.save(picture_path)
    return picture_fn


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
                {url_for('users.reset_token', token=token, _external=True)}
                
                If you did not make this request then simply ignore this email and no changes will be made.
                '''
    mail.send(msg)

def delete_picture(path, image_name):
    try:
        picture_path = os.path.join(current_app.root_path, path, image_name)
        os.remove(picture_path)
    except:
        print("cant delete image from datapase")

