
import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flaskblog import mail
from io import BytesIO
import base64
import tempfile



def save_profile_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    # Open the image
    i = Image.open(form_picture)

    # Get the original image dimensions
    w, h = i.size
    smaller_size = w if w < h else h

    # Define the crop area to make the image square
    crop_area = (0, 0, smaller_size, smaller_size)
    i = i.crop(crop_area)

    # Define the output size and resize the image using LANCZOS filter
    output_size = (125, 125)
    i.thumbnail(output_size, Image.Resampling.LANCZOS)

    # Save the image
    i.save(picture_path)

    return picture_fn

FILEBASE_GATEWAY_URL = os.getenv("FILEBASE_GATEWAY_URL")
def get_filebase_image_url(image_url_id):
    return f"{FILEBASE_GATEWAY_URL}{image_url_id}"

def save_blog_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/post_pics', picture_fn)
    i = Image.open(form_picture)
    i.save(picture_path)
    return picture_fn
def store_file_to_temp_folder(form_picture, file_ext = ".png"):
    with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext, mode="w") as temp_file:
        filename = temp_file.name
        i = Image.open(form_picture)
        i.save(filename)
        temp_file.flush()
        temp_file.seek(0)
        temp_file.close()
    return filename

def convert_picture_to_byte(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    #picture_path = os.path.join(current_app.root_path, 'static/post_pics', picture_fn)
    i = Image.open(form_picture)
    #i.save(picture_path)
    format_type = "JPEG" if f_ext.lower() in ['.jpg', '.jpeg'] else "PNG"
    img_bytes = BytesIO()
    i.save(img_bytes, format=i.format)  # Save in the original format
    img_bytes.seek(0)
    binary_data = img_bytes.getvalue()
    # Convert binary data to Base64 string
    image_base64 = base64.b64encode(binary_data).decode('utf-8')
    return f"data:image/{format_type.lower()};base64,{image_base64}", picture_fn


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

