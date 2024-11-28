import os
from flask_bcrypt import Bcrypt
from flaskblog.service_layer.database_repository.mongo_db import MongoDB
bcrypt = Bcrypt()


db_name = os.getenv("MONGO_DB_NAME")
db = MongoDB(db_name)

def test_insert_admin_role():
    password = "admin"
    hashed_password = bcrypt.generate_password_hash(password=password).decode('utf-8')
    db.insert_document("users", {
        'username': 'admin',
        'password': hashed_password,
        'email': 'admin@admin.com',
        'legal_name': "admin",
        "image_file": "test.png"

    })

def test_edit_admin_role():
    db.update_document("users",{'username':'admin'}, {
        'email':'admin@admin.com',
        'legal_name': "admin",
        "image_file": "test.png"
    })