# Personal Blog

## Quick Start - localy:

	git clone -b v1.0 https://github.com/yaruchyo/PersonalBlog.git
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
Default settings:

`login:admin`
`password:admin`

After loging the password, admin username and Email can be changed on the page [Account](http://localhost:5000/account "Account").

New posts can be added by switching to the tab [New Post](http://localhost:5000/post/new "New Post")

*IMPORTANT!*

in the `Content` section, the `HTML` text has to be inserted!
All pictures in content field have to be uploaded first in the [Images](http://localhost:5000/upload_images "Images") tab.

Images into post can be linked like:

`<img src="http://localhost:5000/static/post_pics/23d2544e7ed4310a.jpg"  alt="">`

Where the image name can be found on the [Images](http://localhost:5000/upload_images "Images") tab.

The html template is open source project and can be viewed: [Philosophy Demo](https://colorlib.com/wp/template/philosophy/ "Philosophy Demo")

------------



