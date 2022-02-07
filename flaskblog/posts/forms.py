from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from wtforms.fields import MultipleFileField


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()], render_kw={"placeholder": "Title"})
    description = TextAreaField('Description', validators=[DataRequired()], render_kw={"placeholder": "Description"})
    content = TextAreaField('Content', validators=[DataRequired()], render_kw={"placeholder": "Content"})
    picture = FileField('Update Main Block Picture', validators=[DataRequired(), FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Create')


class PostUpdateForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    picture = FileField('Update Main Block Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')


class UploadPostImagesForm(FlaskForm):
    picture = MultipleFileField('Upload Image to last post', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Upload')