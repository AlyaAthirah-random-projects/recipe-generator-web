import os
from apps.home import blueprint
from flask import render_template, request, redirect, url_for
from jinja2 import TemplateNotFound
import psycopg2
from werkzeug.utils import secure_filename
from openai import OpenAI
from src import ProcessImage
from src import ResizeImage
from src import GptApi
from src import AnythingApi
from src.ProcessImage import process_receipt_image

dbname=os.getenv("DB_NAME")
dbuser=os.getenv("DB_USERNAME")
dbpass=os.getenv("DB_PASS")
dbhost=os.getenv("DB_HOST")
conn = psycopg2.connect(f"dbname={dbname} user={dbuser} password={dbpass} host={dbhost}")

image_arr = []
generated_recipe = ""

@blueprint.route('/index')
# @login_required
def index():
    return render_template('home/index.html', segment='index')


@blueprint.route('/<template>')
# @login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("pages/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500

@blueprint.route('/groceries')
def grocery_list():
    cur = conn.cursor()
    cur.execute("SELECT * FROM items")
    groceries = cur.fetchall()
    cur.close()

    return render_template('pages/tables-data.html', groceries=groceries)

@blueprint.route('/recipe')
def recipe():
    if generated_recipe:
        return render_template('pages/generate-recipe.html', recipeText=generated_recipe)
    else:
        return render_template('pages/generate-recipe.html')

@blueprint.route('/recipe-generate-gpt', methods=['GET', 'POST'])
def recipe_generator_gpt():
    global generated_recipe

    if request.method == 'POST':
        ingredients = request.form['ingredients']
        prompt = request.form['prompt']

        # Call GPT to generate the recipe
        generated_recipe = GptApi.gpt_generate_recipe(ingredients, prompt)

    return redirect((url_for('home_blueprint.recipe')))

@blueprint.route('/recipe-generate-llama', methods=['GET', 'POST'])
def recipe_generator_llama():
    global generated_recipe

    if request.method == 'POST':
        prompt = request.form['dish']

        # Call GPT to generate the recipe
        generated_recipe = AnythingApi.get_recipe(prompt)
        generated_recipe = generated_recipe.replace('\n', '<br>')

    return redirect((url_for('home_blueprint.recipe')))

@blueprint.route('/upload-receipt')
def upload_receipt_page():
    if image_arr is None:
        print("go through here")
        return render_template('pages/upload-receipt.html')
    else:
        # print("go through here")
        return render_template('pages/upload-receipt.html', images=image_arr)


@blueprint.route('/upload', methods=['POST'])
def upload_receipt():
    global image_arr
    if 'file' not in request.files:
        return "No file part"

    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('home_blueprint.upload_receipt_page'))

    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join('uploads/', filename)
        file.save(filepath)

        # Try the resize image
        ResizeImage.resize_image(filepath, 1200)

        # Process the receipt with OpenAI GPT to get JSON format
        receipt_text, image_byte = ProcessImage.process_receipt_image(filepath)
        image_arr = image_byte
        grocery_items = ProcessImage.gpt_process_receipt(receipt_text)

        # Insert into PostgreSQL
        ProcessImage.save_to_database(grocery_items)

        if image_arr:
            print("imageArr exists")
            return redirect(url_for('home_blueprint.upload_receipt_page'))
        else:
            return redirect(url_for('home_blueprint.grocery_list'))


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
