# Personal Blog

## EC2:
    source ./myenv/bin/activate
    nohup gunicorn run:app --bind 0.0.0.0:8080 &
    sudo kill -9 $(sudo lsof -t -i:8080)

## Quick Start - localy:

	cd PersonalBlog
	python3 -m venv venv
	source venv/bin/activate
	pip3 install -r requirements.txt
	export FLASK_ENV=production
	export FLAS_APP=run.py
	flask run

## Quick Start - Docker:
	
	cd docker_script
	docker_compose up -d

------------
## Description:

This project is ready to use for creating personal blog. After running the `run.py` script, admin page can be accessed by redirecting to [localhost:5000/admin](http://localhost:5000/admin "localhost:5000/admin")

Default settings are:

`login:admin`
`password:admin`

After signing up as admin rights, password, admin username and Email can be changed on the page [Account](http://localhost:5000/account "Account").

New posts can be added by switching to the tab [New Post](http://localhost:5000/post/new "New Post")

*IMPORTANT!*

in the `Content` section, the `HTML` text has to be inserted!
All pictures in content field have to be uploaded first in the [Images](http://localhost:5000/upload_images "Images") tab.

Images into post can be linked like:

`<img src="http://localhost:5000/static/post_pics/23d2544e7ed4310a.jpg"  alt="">`

Where the image name can be found on the [Images](http://localhost:5000/upload_images "Images") tab.

The html template is open source project and can be viewed: [Philosophy Demo](https://colorlib.com/wp/template/philosophy/ "Philosophy Demo")

This project was created by rectiating following youtube tutorials:

- [Learning Flask](https://www.youtube.com/watch?v=BUmUV8YOzgM&list=PLF2JzgCW6-YY_TZCmBrbOpgx5pSNBD0_L "Learning Flask")
- [Python Flask Tutorial](https://www.youtube.com/watch?v=MwZwr5Tvyxo&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH "Python Flask Tutorial")
------------

### Posts
All posts can be updating without changing the creatin date, so post order will stay remain.
There is also oportunity to delete posts from main page.

### Registration
New users can be added to the database, so there can be not only one `admin`


