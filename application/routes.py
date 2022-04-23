from flask import render_template, request, url_for, redirect, flash
from application import app, db, bcrypt
from application.forms import IngredientsForm, UserAccountForm, UserLoginForm
from application.models import Ingredient, IngredientRecipe, Recipe, Instruction, Difficulty, User
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/home", methods=["GET", "POST"])
@app.route("/", methods=["GET", "POST"])
def home():
    error = ""
    form = IngredientsForm()

    if request.method == "POST":
        ingredient_result = form.ingredients.data

        if len(ingredient_result) == 0:
            error = "Please supply an ingredient"
        else:

            # stuff = Ingredient.query.filter_by(ingredient_name="Avocado").all()
            # return str(stuff)

            # return ingredient_result
            stuff = Ingredient.query.all()
            # stuff = Ingredient.query.filter_by(ingredient_name=ingredient_result)
            return str(stuff)

            # trialling out queries below
            # query_result = db.execute("SELECT ingredient_name FROM ingredient WHERE ingredient_name = :ingredient_result", {"ingredient_result": ingredient_result})
            # return query_result
            # Ingredient.query.filter_by(ingredient_name=ingredient_result).first()
            # ingredient_id = Ingredient.query.get(ingredient_name)
            # query = Ingredient.query.get(ingredient_id)
            # return query

    return render_template('home.html', form=form, message=error)


@app.route("/recipe", methods=["GET", "POST"])
def recipe():
    return render_template('recipe.html')


@app.route("/about", methods=["GET"])
def about():
    url = url_for('home')
    return render_template('about.html', title='about', page_title=url)


@app.route("/resources", methods=["GET"])
def resources():
    return render_template('resources.html')


@app.route("/blog", methods=["GET", "POST"])
def blog():
    return render_template('blog.html')


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = UserAccountForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(first_name=form.first_name.data, last_name=form.last_name.data, username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created. You can log in using your email and password", "success")
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = UserLoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check email and password')
    return render_template('login.html', title='Login', form=form)


@app.route("/useraccount")
@login_required
def user_account():
    return render_template('useraccount.html', title='Account')


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/contact", methods=["GET", "POST"])
def contact():
    return render_template('contact.html')


# # PREVIOUS CODE BEFORE CHARLOTTE COMMIT IS COMMENTED BELOW
# @app.route("/account", methods=["GET", "POST"])
# def account():
#     error = ""
#     form = UserAccountForm()
#
#     if request.method == 'POST':
#         first_name = form.first_name.data
#         last_name = form.last_name.data
#         username = form.username.data
#         email = form.email.data
#         password = form.password.data
#
#         if len(first_name) == 0 or len(last_name) == 0 or len(username) == 0 or len(email) == 0 or len(password) == 0:
#             error = "Please supply requested contact information"
#         else:
#             person = User(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
#             db.session.add(person)
#             db.session.commit()
#             return 'Thank you!'
#
#     return render_template('register.html', title="Register", form=form, message=error)
#
#
# @app.route("/login", methods=["GET", "POST"])
# def login():
#     error = ""
#     form = UserLoginForm()
#
#     if request.method == 'POST':
#         email = form.email.data
#         password = form.password.data
#
#         if len(email) == 0 or len(password) == 0:
#             error = "Please supply requested log in details"
#         #   password validation needed here!
#         #   filter user table by password to allow user to log in
#         else:
#             # link to user's account page
#             return 'Access granted!'
#
#     return render_template('login.html', title="Register", form=form, message=error)