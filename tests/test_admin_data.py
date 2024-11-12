
from flask_bcrypt import Bcrypt
from tests.mongo_db import MongoDB
bcrypt = Bcrypt()


db_name = "db_test"
#db_collection = "collection_test"
db = MongoDB(db_name)

def test_insert_admin_role():
    password = "admin"
    hashed_password = bcrypt.generate_password_hash(password=password).decode('utf-8')
    db.insert_document("users", {'username':'admin', 'password': hashed_password})

def test_edit_admin_role():
    db.update_document("users",{'username':'admin'}, {'email':'admin@admin.com'})