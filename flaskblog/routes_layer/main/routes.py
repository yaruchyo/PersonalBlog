from flask import render_template, request, Blueprint
from flaskblog.service_layer.models import Post

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.get_paginated_posts(page)
    posts = [{"id": post['_id'], **post} for i, post in enumerate(posts)]
    #todo work with multiple pages
    if not posts:
        return render_template('errors/create_admin.html')
    return render_template('home.html', posts=posts, total_pages=1, home_page=True)


# @main.route("/about")
# def about():
#     return render_template('about.html', title='About')

