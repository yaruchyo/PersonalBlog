from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post, Images
from flaskblog.posts.forms import PostForm, PostUpdateForm, UploadPostImagesForm
from flaskblog.users.utils import save_blog_picture

posts = Blueprint('posts', __name__)

@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        picture_file = save_blog_picture(form.picture.data)
        post = Post(title=form.title.data, description=form.description.data, content=form.content.data,
                    image_file=picture_file, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')

@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostUpdateForm()
    if form.validate_on_submit():
        print(form.picture.data)
        if form.picture.data:
            picture_file = save_blog_picture(form.picture.data)
            post.image_file = picture_file
        post.title = form.title.data
        post.description = form.description.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.description.data = post.description
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))


@posts.route("/upload_images", methods=['GET', 'POST'])
@login_required
def upload_images():
    page = request.args.get('page', 1, type=int)
    images = Images.query.order_by(Images.date_posted.desc()).paginate(page=page, per_page=10)
    form = UploadPostImagesForm()
    if form.validate_on_submit():
        files_filenames = []
        for img in form.picture.data:
            picture_file = save_blog_picture(img)
            files_filenames.append(picture_file)
        for picture_file in files_filenames:
            image = Images(image_file=picture_file)
            db.session.add(image)
        db.session.commit()
        return redirect(url_for('main.home'))
    return render_template('upload_images.html', form=form, images=images)
