
from flaskblog.models import Images, Post
from flaskblog import create_app

app = create_app()

def test_main():
    page = 1
    with app.app_context():
        posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=20)
        print(posts.items)
        images = Images.query.order_by(Images.date_posted.desc()).paginate(page=page, per_page=10)
        print(images.items)



