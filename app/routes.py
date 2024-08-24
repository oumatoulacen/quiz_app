from flask import render_template, url_for, flash, redirect, request, Blueprint
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask_login import login_user
from flask_login import logout_user
from flask_login import current_user, login_required
from flask import jsonify
from .utils import admin_required

from .models import db, Quiz, Question, Response, QuizResult, User, Category
from .forms import LoginForm, QuizForm, RegistrationForm, CategoryForm, QuestionForm

main = Blueprint('main', __name__)

# register a new user
@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('main.home'))
    return render_template('auth/register.html', form=form)

# login a user
@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('You have been logged in!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('auth/login.html', form=form)

# logout a user
@main.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.home'))


# Dashboard
@main.route('/dashboard')
@login_required
@admin_required
def dashboard():
    return render_template('admin/dashboard.html')

# Profile
@main.route('/profile')
@login_required
def profile():
    user = User.query.get_or_404(current_user.id)
    quiz_results = QuizResult.query.filter_by(user_id=current_user.id).all()
    return render_template('profile.html', user=user, quiz_results=quiz_results)


# home page (list all quizzes)
@main.route('/')
def home():
    quizzes = Quiz.query.all()
    return render_template('home.html', quizzes=quizzes)


# create a new category
@main.route('/admin/add_category', methods=['GET', 'POST'])
@login_required
@admin_required
def add_category():
    form = CategoryForm()
    if form.validate_on_submit():
        # check if category already exist
        if Category.query.filter_by(name=form.name.data):
            return jsonify({ "message": "category already exist"})
        
        category = Category(name=form.name.data)
        db.session.add(category)
        db.session.commit()
        flash('Category added successfully.', 'success')
        return redirect(url_for('main.categories'))
    return render_template('admin/add_category.html', form=form)


# update a category
@main.route('/admin/update_category/<int:category_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def update_category(category_id):
    category = Category.query.get_or_404(category_id)
    form = CategoryForm(obj=category)
    if form.validate_on_submit():
        category.name = form.name.data
        db.session.commit()
        flash('Category updated successfully.', 'success')
        return redirect(url_for('main.categories'))
    return render_template('admin/update_category.html', form=form)

# delete a category
@main.route('/admin/delete_category/<int:category_id>')
@login_required
@admin_required
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    flash('Category deleted successfully.', 'success')
    return redirect(url_for('main.categories'))

# view all categories
@main.route('/admin/categories')
@login_required
@admin_required
def categories():
    categories = Category.query.all()
    return render_template('admin/categories.html', categories=categories)


# create a new quiz
@main.route('/admin/add_quiz', methods=['GET', 'POST'])
@login_required
@admin_required
def add_quiz():
    form = QuizForm()
    if form.validate_on_submit():
        # check if quiz already exist
        if Quiz.query.filter_by(title=form.title.data).first():
            return jsonify({ "message": "quiz already exist"})
        
        quiz = Quiz(
            title=form.title.data,
            description=form.description.data,
            category_id=form.category_id.data
        )
        db.session.add(quiz)
        db.session.commit()
        flash('Quiz added successfully.', 'success')
        return redirect(url_for('main.quizzes'))
    return render_template('admin/add_quiz.html', form=form)

# update a quiz
@main.route('/admin/update_quiz/<int:quiz_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def update_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    form = QuizForm(obj=quiz)
    if form.validate_on_submit():
        quiz.title = form.title.data
        quiz.description = form.description.data
        quiz.category_id = form.category_id.data
        db.session.commit()
        flash('Quiz updated successfully.', 'success')
        return redirect(url_for('main.quizzes'))
    return render_template('admin/update_quiz.html', form=form)

# delete a quiz
@main.route('/admin/delete_quiz/<int:quiz_id>')
@login_required
@admin_required
def delete_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    db.session.delete(quiz)
    db.session.commit()
    flash('Quiz deleted successfully.', 'success')
    return redirect(url_for('main.quizzes'))

# view all quizzes
@main.route('/admin/quizzes')
@login_required
@admin_required
def quizzes():
    quizzes = Quiz.query.all()
    return render_template('admin/quizzes.html', quizzes=quizzes)

# get or submit a quiz
@main.route('/quiz/<int:quiz_id>', methods=['GET', 'POST'])
@login_required
def quiz(quiz_id):
    form = QuestionForm()
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = Question.query.filter_by(quiz_id=quiz.id).all()

    if request.method == 'POST':
        if quiz.total_questions == 0:
            flash('No questions available for this quiz.', 'danger')
            return redirect(url_for('main.quiz', quiz_id=quiz.id))
        # check if quiz_result for the quiz already exists to update it
        quiz_result = QuizResult.query.filter_by(quiz_id=quiz.id, user_id=current_user.id).first()
        if quiz_result:
            print('quiz_result', quiz_result)
            quiz_result_id = quiz_result.id
        else:
            # get the last quiz_result_id and increment it by 1 to get the new quiz_result_id
            # QuizResult.query.delete() # delete all quiz results (if you want to reset the quiz results)
            quiz_result_id = QuizResult.query.count() + 1

        score = 0
        responses = [] 

        # delete existing responses
        try:
            resps = Response.query.filter_by(quiz_id=quiz.id, user_id=current_user.id).delete()
            db.session.commit()
        except:
            pass

        for question in questions:
            selected_option = int(request.form.get(f'question_{question.id}'))
            is_correct = selected_option == question.correct_option

            # Track response
            response = Response(
                user_id=current_user.id,
                quiz_id=quiz.id,
                question_id=question.id,
                selected_option=selected_option,
                is_correct=is_correct,
                quiz_result_id=quiz_result_id
            )
            responses.append(response)
            db.session.add(response)

            # Update score
            if is_correct:
                score += 1

        if quiz_result:
            quiz_result.score=score
            quiz_result.user_id=current_user.id
            quiz_result.quiz_id=quiz.id
        else:
            print('quiz_result_id', quiz_result_id)
            # Store quiz result
            quiz_result = QuizResult(
                id=quiz_result_id,
                score=score,
                user_id=current_user.id,
                quiz_id=quiz.id
            )
            db.session.add(quiz_result)
        db.session.commit()

        flash(f'Your score: {score}/{len(questions)}', 'success')
        return redirect(url_for('main.quiz_result', quiz_result_id=quiz_result.id))
    return render_template('quiz.html', quiz=quiz, questions=questions, form=form)




# create a new question
@main.route('/admin/add_question', methods=['GET', 'POST'])
@login_required
@admin_required
def add_question():
    form = QuestionForm()
    if form.validate_on_submit():
        quiz = Quiz.query.get_or_404(form.quiz_id.data)
        if Question.query.filter_by(text=form.text.data).first():
            return jsonify({ "message": "question already exist"})
        question = Question(
            text=form.text.data,
            options=form.options.data,
            correct_option=form.correct_option.data,
            quiz_id=form.quiz_id.data
        )
        # Update quiz total questions
        quiz.total_questions += 1
        db.session.commit()

        db.session.add(question)
        db.session.commit()
        flash('Question added successfully.', 'success')
        return redirect(url_for('main.questions'))
    return render_template('admin/add_question.html', form=form)

# update a question
@main.route('/admin/update_question/<int:question_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def update_question(question_id):
    question = Question.query.get_or_404(question_id)
    form = QuestionForm(obj=question)
    if form.validate_on_submit():
        question.text = form.text.data
        question.options = form.options.data
        question.correct_option = form.correct_option.data
        question.quiz_id = form.quiz_id.data
        db.session.commit()
        flash('Question updated successfully.', 'success')
        return redirect(url_for('main.questions'))
    return render_template('admin/update_question.html', form=form)


# delete a question
@main.route('/admin/delete_question/<int:question_id>')
@login_required
@admin_required
def delete_question(question_id):
    question = Question.query.get_or_404(question_id)
    quiz = Quiz.query.get_or_404(question.quiz_id)
    quiz.total_questions -= 1
    db.session.delete(question)
    db.session.commit()
    flash('Question deleted successfully.', 'success')
    return redirect(url_for('main.questions'))

# view all questions
@main.route('/admin/questions')
@login_required
@admin_required
def questions():
    quizzes = Quiz.query.all()
    return render_template('admin/questions.html', quizzes=quizzes)



# get quiz results
@main.route('/quiz_result/<int:quiz_result_id>')
@login_required
def quiz_result(quiz_result_id):
    # get the quiz_result of the current user
    quiz_result = QuizResult.query.filter_by(id=quiz_result_id, user_id=current_user.id).first()
    if not quiz_result:
        flash('Quiz result not found.', 'danger')
        return redirect(url_for('main.home'))
    return render_template('quiz_result.html', quiz_result=quiz_result)

# delete a quiz result
@main.route('/admin/delete_quiz_result/<int:quiz_result_id>')
@login_required
def delete_quiz_result(quiz_result_id):
    quiz_result = QuizResult.query.filter_by(id=quiz_result_id, user_id=current_user.id).first()
    if not quiz_result:
        flash('Quiz result not found.', 'danger')
        return redirect(url_for('main.home'))
    db.session.delete(quiz_result)
    db.session.commit()
    flash('Quiz result deleted successfully.', 'success')
    return redirect(url_for('main.profile'))