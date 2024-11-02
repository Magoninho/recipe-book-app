from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from . import db
from .models import Recipe, User, Category
import datetime

bp = Blueprint('recipes', __name__, url_prefix='/recipes')


@bp.route('/', methods=['GET'])
@login_required
def home():

    query = (
        db.session.query(
            Recipe.id,
            Recipe.title,
            Recipe.ingredients,
            Recipe.steps,
            Recipe.date_created,
            Recipe.image_path,
            Category.name.label("category_name")
        )
        .join(Category, Recipe.category_id == Category.id)
    )
    recipes = query.all()
    
    return render_template('home.html', recipes=recipes)

@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'GET':
        categories = Category.query.all()
        return render_template('create_recipe.html', categories=categories)
    else:
        title = request.form.get('title')
        ingredients = request.form.get('ingredients')
        steps = request.form.get('steps')
        category_id = request.form.get('category')

        current_date = datetime.datetime.now()
        new_recipe = Recipe(user_id=current_user.id, title=title, ingredients=ingredients, steps=steps, date_created=current_date, category_id=category_id)

        db.session.add(new_recipe)
        db.session.commit()

        return redirect(url_for('recipes.home'))

@bp.route('/update/<int:recipe_id>', methods=['GET', 'POST'])
@login_required
def edit(recipe_id):
    recipe = Recipe.query.filter_by(id=recipe_id).first()
    categories = Category.query.all()
    if request.method == 'GET':
        return render_template('edit_recipe.html', recipe=recipe, categories=categories)
    elif request.method == 'POST':
        recipe.title = request.form.get('title')
        recipe.ingredients = request.form.get('ingredients')
        recipe.steps = request.form.get('steps')
        recipe.category_id = request.form.get('category')

        db.session.commit()
        return redirect(url_for('recipes.home'))