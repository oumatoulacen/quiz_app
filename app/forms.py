from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField,  IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from wtforms.fields import FieldList
 

from .models import User, Category, Quiz

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already registered. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class CategoryForm(FlaskForm):
    name = StringField('Category Name', validators=[DataRequired(), Length(min=2, max=100)])
    submit = SubmitField('Add Category')

class QuizForm(FlaskForm):
    title = StringField('Quiz Title', validators=[DataRequired(), Length(min=2, max=200)])
    description = StringField('Description', validators=[DataRequired(), Length(min=10, max=500)])
    category_id = SelectField('Category', coerce=int)
    submit = SubmitField('Add Quiz')
    total_questions = IntegerField('Total Questions', validators=[DataRequired(), NumberRange(min=0, max=100)])

    # Populate the category choices from the database when the form is created(this technique is called lazy loading)
    def __init__(self, *args, **kwargs):
        super(QuizForm, self).__init__(*args, **kwargs)
        self.category_id.choices = [(c.id, c.name) for c in Category.query.all()]

class QuestionForm(FlaskForm):
    text = StringField('Question Text', validators=[DataRequired(), Length(min=5, max=500)])
    options = FieldList(StringField('Option', validators=[DataRequired(), Length(min=1, max=200)]), min_entries=4, max_entries=4)
    correct_option = IntegerField('Correct Option Index', validators=[DataRequired(), NumberRange(min=1, max=4)])
    quiz_id = SelectField('Quiz', coerce=int)
    submit = SubmitField('Add Question')

    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.quiz_id.choices = [(q.id, q.title) for q in Quiz.query.all()]