from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post, Images
from flaskblog.posts.forms import PostForm, PostUpdateForm, UploadPostImagesForm
from flaskblog.users.utils import save_blog_picture, delete_picture
from bson import ObjectId
from math import ceil

posts = Blueprint('posts', __name__)

@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        picture_file = save_blog_picture(form.picture.data)
        post = Post(title=form.title.data, description=form.description.data, content=form.content.data,
                    image_file=picture_file, author=current_user)
        post.save()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')

@posts.route("/post/<int:post_id>")
def post(post_id):
    post = db.find_document("posts", {"_id": post_id})
    if not post:
        abort(403)
    user = db.find_document('users',  {"_id": ObjectId( post['author'])})
    post['author_name'] = user['legal_name']
    return render_template('post.html', title=post['title'], post=post)

@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = db.find_document('posts', {'_id': post_id})
    if post['author'] != current_user.id:
        abort(403)
    form = PostUpdateForm()
    print(form.picture.data)
    if form.validate_on_submit():

        if form.picture.data:
            picture_file = save_blog_picture(form.picture.data)
            post['image_file'] = picture_file
        post['title'] = form.title.data
        post['description'] = form.description.data
        post['content'] = form.content.data
        db.update_document('posts', {'_id': post_id}, post)
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post['_id']))
    elif request.method == 'GET':
        form.title.data = post['title']
        form.description.data = post['description']
        form.content.data = post['content']
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = db.find_document('posts', {'_id': post_id})
    if post['author'] != current_user.id:
        abort(403)
    delete_picture('static/post_pics', post['image_file'])
    db.delete_documents('posts', {'_id': post_id})
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))


@posts.route("/upload_images", methods=['GET', 'POST'])
@login_required
def upload_images(per_page=25):
    images = db.find_documents('images', {})
    images = [{**image, "_id": index} for index, image in enumerate(images)]
    total_images = db.count_documents("images")
    current_page = request.args.get('page', 1, type=int)
    total_pages = ceil(total_images / per_page)
    form = UploadPostImagesForm()
    if form.validate_on_submit():

        files_filenames = []
        for img in form.picture.data:
            picture_file = save_blog_picture(img)
            files_filenames.append(picture_file)
        for picture_file in files_filenames:
            image = Images(image_file=picture_file)
            image.save()
        return redirect(url_for('posts.upload_images'))
    return render_template('upload_images.html', form=form, images=images, total_pages=total_pages, current_page=current_page)
