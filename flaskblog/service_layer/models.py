import os
from datetime import datetime
from itsdangerous import TimedSerializer as Serializer
from flaskblog import db, login_manager, file_storage
from flask import current_app
from flask_login import UserMixin
from bson.objectid import ObjectId


@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)

class User(UserMixin):
    def __init__(self, user_data, image_file="default.jpg"):
        self.id = str(user_data['_id'])
        self.username = user_data['username']
        self.legal_name = user_data['legal_name']
        self.email = user_data['email']
        self.password = user_data['password']
        self.image_file = user_data['image_file']
        self.posts = []  # store post ids to reference posts
        self.active = user_data.get('active', True)

    def save(self):
        # Insert the user document into MongoDB
        db.insert_document(self.__dict__)
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': str(self._id)}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.get_by_id(user_id)

    @staticmethod
    def get_by_id(user_id):
        user_data = db.find_document('users', {"_id": ObjectId(user_id)})
        if user_data:
            user = User(user_data)
            return user
        return None

    @property
    def is_active(self):
        # This property checks if the user is active
        return self.active

    @property
    def is_authenticated(self):
        # This property must return True if the user is authenticated
        return True

    @property
    def is_active(self):
        # This property checks if the user is active
        return self.active

    @property
    def is_anonymous(self):
        # This should return False as the user is not anonymous
        return False

    def get_id(self):
        # This should return a string representing the user's ID
        return self.id

    @staticmethod
    def get_user_by_username(username):
        return db.find_document('users', {'username': username})

    @staticmethod
    def get_user_by_email(email):
        return db.find_document('users', {'email': email})

    @staticmethod
    def update_user_data(current_user):
        db.update_document('users',
                           {'_id': ObjectId(current_user.id)},
                           {
                                "password": current_user.password,
                                "email": current_user.email,
                                "username": current_user.username,
                                "image_file": current_user.image_file,
                                "legal_name": current_user.legal_name
                           })

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Post:
    def __init__(self, title, description, content, author, image_url, image_filename):
        self._id = db.get_max_id('posts', {}) + 1
        self.title = title
        self.date_posted = datetime.utcnow()
        self.description = description
        self.content = content
        self.image_url = image_url
        self.image_filename=image_filename
        self.author = author.id  # store user id as reference

    @staticmethod
    def get_paginated_posts(page: int, per_page: int = 20):
        # Order by `date_posted` in descending order, skip (page - 1) * per_page documents, and limit to `per_page`
        skip = (page - 1) * per_page
        results = db.find_sorted_documents("posts", {}, per_page, skip)
        return list(results)

    def save(self):
        # Insert the post document into MongoDB
        db.insert_document('posts', self.__dict__)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


class Images:
    def __init__(self, image_url, image_filename ="default.jpg"):
        self.date_posted = datetime.utcnow()
        self.image_filename = image_filename
        self.image_url = image_url

    def save(self):
        # Insert the image document into MongoDB
        db.insert_document('images', self.__dict__)

    def __repr__(self):
        return f"Image('{self.image_filename}', '{self.date_posted}')"

