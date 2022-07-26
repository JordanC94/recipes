from flask import render_template, request, redirect, session
from flask_app import app
from flask_app.models.recipe import Recipe

# ! ////// CREATE  //////
# TODO CREATE REQUIRES TWO ROUTES:
# TODO ONE TO DISPLAY THE FORM:
@app.route('/recipe/new')
def new_recipe():
    if 'user_id' not in session:
        return redirect('/logout')
    return render_template("new_recipe.html")

# TODO ONE TO HANDLE THE DATA FROM THE FORM
@app.route('/recipe/create',methods=['POST'])
def create_recipe():
    if not Recipe.validate_recipe(request.form):
        return redirect('/recipe/new')
    print(request.form)
    
    Recipe.save(request.form)
    return redirect('/recipes')

# TODO READ ALL
@app.route('/recipes')
def recipes():
    if 'user_id' not in session:
        return redirect('/logout')
    return render_template("recipes.html",recipes=Recipe.get_all_with_recipe())

# TODO READ ONE
@app.route('/recipe/show/<int:id>')
def show_recipes(id):
    data ={ 
        "id":id
    }
    return render_template("show_recipe.html",recipe=Recipe.get_one(data))

# ! ///// UPDATE /////
# TODO UPDATE REQUIRES TWO ROUTES
# TODO ONE TO SHOW THE FORM
@app.route('/recipe/edit/<int:id>')
def edit_recipe(id):
    data ={ 
        "id":id
    }
    return render_template("edit_recipe.html",recipe=Recipe.get_one(data))

# TODO ONE TO HANDLE THE DATA FROM THE FORM
@app.route('/recipe/update',methods=['POST'])
def update_recipe():
    if not Recipe.validate_recipe(request.form):
        return redirect(f"/recipe/edit/{request.form['id']}")
    Recipe.update(request.form)
    return redirect('/recipes')

# ! ///// DELETE //////
@app.route('/recipe/destroy/<int:id>')
def destroy_recipe(id):
    data ={
        'id': id
    }
    Recipe.destroy(data)
    return redirect('/recipes')