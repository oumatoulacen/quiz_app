from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from . import db


# User model
class User(db.Model, UserMixin):
    ''' Represents the users. Each user has quiz results. '''
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(220), nullable=False)
    quiz_results = db.relationship('QuizResult', backref='user', lazy=True)
    is_admin = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f'<User {self.username}>'

# Category model
class Category(db.Model):
    ''' Represents categories for quizzes (e.g., Science, History) '''
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    # delete quizzes when a category is deleted
    quizzes = db.relationship('Quiz', backref='category', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Category {self.name}>'

# Quiz model
class Quiz(db.Model):
    ''' Represents the quizzes. Each quiz has multiple questions and is associated with a category.'''
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    total_questions = db.Column(db.Integer, nullable=False, default=0)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    questions = db.relationship('Question', backref='quiz', lazy=True, cascade='all, delete-orphan')

    quiz_results = db.relationship('QuizResult', backref='quiz', lazy=True, cascade='all, delete-orphan')

    def is_completed_by(self, user):
        ''' Check if the quiz has been completed by the user. '''
        return QuizResult.query.filter_by(user_id=user.id, quiz_id=self.id).first() is not None and self.total_questions == self.get_user_score(user)

    def get_user_score(self, user):
        ''' Get the score of the user for this quiz. '''
        quiz_result = QuizResult.query.filter_by(user_id=user.id, quiz_id=self.id).first()
        return quiz_result.score if quiz_result else 0
    
    def is_started_by(self, user):
        ''' Check if the quiz has been taken by the user. '''
        return QuizResult.query.filter_by(user_id=user.id, quiz_id=self.id).first() is not None and self.total_questions != self.get_user_score(user)

    def get_result_id(self, user):
        ''' Get the result id of the user for this quiz. '''
        quiz_result = QuizResult.query.filter_by(user_id=user.id, quiz_id=self.id).first()
        return quiz_result.id if quiz_result else 0

    def __repr__(self):
        return f'<Quiz {self.title}>'


# Question model
class Question(db.Model):
    ''' Represents the questions for a quiz. Each question has multiple options and one correct option.'''
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=False)
    options = db.Column(db.JSON, nullable=False)  # Store options as JSON
    correct_option = db.Column(db.Integer, nullable=False)  # Store index of correct option
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)

    # delete responses when a question is deleted
    responses = db.relationship('Response', backref='question', lazy=True, cascade='all, delete-orphan')
    def __repr__(self):
        return f'<Question {self.text}>'

# Response model
class Response(db.Model):
    ''' Tracks user responses to questions, including the selected option and whether it was correct. Responses are linked to users, quizzes, and questions. '''
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    selected_option = db.Column(db.Integer, nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False)
    quiz_result_id = db.Column(db.Integer, db.ForeignKey('quiz_result.id'), nullable=False)

    user = db.relationship('User', backref='responses')
    quiz = db.relationship('Quiz', backref='responses')


    def __repr__(self):
        return f'<Response User:{self.user_id} Quiz:{self.quiz_id} Question:{self.question_id} SelectedOption:{self.selected_option}>'

# QuizResult model
class QuizResult(db.Model):
    ''' Represents the results of a user taking a quiz. Includes the score and links to the user and quiz. '''
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    responses = db.relationship('Response', backref='quiz_result', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<QuizResult User:{self.user_id} Quiz:{self.quiz_id} Score:{self.score}>'