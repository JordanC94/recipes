from flask import render_template, request, redirect, session, flash
from flask_app import app, bcrypt
from flask_app.models.user import User

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/register/user", methods=['POST'])
def register():
    print(request.form)
    if not User.validate_user(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password" : pw_hash
    }
    user_id = User.save(data)
    session['user_id'] = user_id
    session['user_name'] = f"{request.form['first_name']} {request.form['last_name']}"
    return redirect('/recipes')

@app.route('/login', methods=['post'])
def login():
    data = {'email': request.form['email']}
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash('invalid credentials')
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash('invalid credentials')
        return redirect('/')
    session['user_id'] = user_in_db.id
    session['user_name'] =f"{user_in_db.first_name} {user_in_db.last_name}" 
    return redirect('/recipes')

@app.route('/user/show/<int:id>')
def user_show(id):
    data = {'id': id}
    
    return render_template('show_user.html', user=User.get_user_with_recipes(data))

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')