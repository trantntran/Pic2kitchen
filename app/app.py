import os
from flask import Flask, render_template
from . import yolo
import numpy as np
import pandas as pd
import json

from gensim.models import KeyedVectors
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from . import video_api

# from flask_login import LoginManager
# from flask_sqlalchemy import SQLAlchemy
# from flask_login import UserMixin
# from sqlalchemy import Binary, Column, Integer, String
# from util import hash_pass,verify_pass
# from forms import LoginForm, CreateAccountForm
from flask import jsonify, render_template, redirect, request, url_for
# from flask_login import (
#     current_user,
#     login_required,
#     login_user,
#     logout_user
# )
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
ROOT_DIR = os.path.abspath('.')
UPLOAD_DIR = os.path.join(ROOT_DIR,'static','images','upload')
model = Doc2Vec.load(".\static\data\d2v_v4.model")
app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_DIR

# db = SQLAlchemy(app)
# login_manager = LoginManager()
# #app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'


# @app.before_first_request
# def initialize_database():
#     db.create_all()


# class User(db.Model, UserMixin):

#     __tablename__ = 'User'

#     id = Column(Integer, primary_key=True)
#     username = Column(String, unique=True)
#     email = Column(String, unique=True)
#     password = Column(Binary)
#     #favorites

#     def __init__(self, **kwargs):
#         for property, value in kwargs.items():
#             # depending on whether value is an iterable or not, we must
#             # unpack it's value (when **kwargs is request.form, some values
#             # will be a 1-element list)
#             if hasattr(value, '__iter__') and not isinstance(value, str):
#                 # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
#                 value = value[0]

#             if property == 'password':
#                 value = hash_pass( value ) # we need bytes here (not plain str)
                
#             setattr(self, property, value)

#     def __repr__(self):
#         return str(self.username)
df_recipe = pd.read_csv('.\static\data\File_name.csv',sep='\t')
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ## Login & Registration

# # check url for
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     login_form = LoginForm(request.form)
#     if 'login' in request.form:
        
#         # read form data
#         username = request.form['username']
#         password = request.form['password']

#         # Locate user
#         user = User.query.filter_by(username=username).first()
        
#         # Check the password
#         if user and verify_pass( password, user.password):
#             # Go to homepage
#             login_user(user)
#             return redirect(url_for('index'))

#         # Something (user or pass) is not ok
#         return render_template( 'login.html', msg='Wrong user or password', form=login_form)

#     if not current_user.is_authenticated:
#         return render_template( 'accounts/login.html',
#                                 form=login_form)
#     return redirect(url_for('index'))

# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     login_form = LoginForm(request.form)
#     create_account_form = CreateAccountForm(request.form)
#     if 'register' in request.form:

#         username  = request.form['username']
#         email     = request.form['email'   ]

#         # Check usename exists
#         user = User.query.filter_by(username=username).first()
#         if user:
#             return render_template( 'accounts/register.html', 
#                                     msg='Username already registered',
#                                     success=False,
#                                     form=create_account_form)

#         # Check email exists
#         user = User.query.filter_by(email=email).first()
#         if user:
#             return render_template( 'register.html', 
#                                     msg='Email already registered', 
#                                     success=False,
#                                     form=create_account_form)

#         # else we can create the user
#         user = User(**request.form)
#         db.session.add(user)
#         db.session.commit()

#         return render_template( 'accounts/register.html', 
#                                 msg='User created please <a href="/login">login</a>', 
#                                 success=True,
#                                 form=create_account_form)

#     else:
#         return render_template( 'accounts/register.html', form=create_account_form)

# @app.route('/logout')
# def logout():
#     logout_user()
#     return redirect(url_for('index'))

# @app.route('/shutdown')
# def shutdown():
#     func = request.environ.get('werkzeug.server.shutdown')
#     if func is None:
#         raise RuntimeError('Not running with the Werkzeug Server')
#     func()
#     return 'Server shutting down...'

def get_current_index():
    try:
        image_path = Path(UPLOAD_DIR)
        image_path = image_path.glob('.')
        image_name = [path.name for path in image_path]
        image_name = [int(name.split('.')[0]) for name in image_name]
        current_index = max(image_name)
    except: 
        current_index = 0
    return current_index

global current_index
current_index = get_current_index()

@app.route('/', methods=['GET', 'POST'])
def index():
    print(request.method)
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            print('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            print('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            global current_index 
            current_index += 1 
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], str(current_index)+".jpg"))
            new_filename = str(current_index)+".jpg" 
            return redirect(url_for('kitchen',filename = new_filename))
    return render_template('index.html')

#
def make_query_string(ingredients):
    query_str =''
    if(len(ingredients)==0):
        return query_str
    elif(len(ingredients)==1):
        query_str = ingredients[0] +' == True'
        return query_str
    else:
        for ingredient in ingredients[:-1]:
            query_str = query_str + ingredient +' == True & '
        query_str = query_str + ingredients[-1] + ' == True'
        return query_str

def Query_index(ingredients,dframe):
    str_query = make_query_string(ingredients)
    result = dframe.query(str_query)['IndexFile']
    print('QUERY', result)
    if(len(result) !=0):
        return result.tolist()
    a =  ingredients[:-1]
    return Query_index(a ,dframe)

def GetFoodRecipe(index):
    name_file = './static/data/Food_recipe/food'+(5-len(str(index)))*'0'+str(index)+'.json'
    print(name_file)
    try:
        with open(name_file) as json_data:
            data = json.load(json_data)
        return data
    except Exception as inst:
        print(index)
        print(type(inst))
        print(inst.args)

##input is list ingredient of food 
##output is index_file (for seach name file ex: food00001.json) top 5 similar
def Doc2Vec_for_ingridient(list_ingredient, model):
    
    vector = model.infer_vector(list_ingredient)
    simmilar = model.docvecs.most_similar([vector], topn=5)
    index_file= []
    for x in simmilar[0]:
        index_file.append(x+1)
    return index_file

def Doc2Vec_for_simila_food(index_doc, model, top_n):
    
    simmilar = model.docvecs.most_similar([model.docvecs[index_doc]], topn=top_n)
    index_file= []
    for x in simmilar[1:]: #bo thang dau tine vi la chinh no
        index_file.append(x[0]+1)
    return index_file
def GetVideo(name):
    # assign some var get response from API below
    video_api.query(name)
    #return output as link video

@app.route('/kitchen/<filename>')
def kitchen(filename):
    ls = []
    PICTURE_DIR = os.path.join(UPLOAD_DIR,filename)
    print(PICTURE_DIR)
    class_obj = yolo.image_detect(PICTURE_DIR)
    print(class_obj)
    if(len(class_obj)== 0):
        return render_template('Error.html')
    else:
        result = Query_index(class_obj,df_recipe)
        print('RESULT', result)
        if(len(result)>=6):
            result = result[:7]
        else:
            new_result = Doc2Vec_for_simila_food(result[0],model,6-len(result)+1)
            for new_re in new_result:
                result.append(new_re)
        print(result)
        for recipe in result:
            data = GetFoodRecipe(recipe)
            data_temp = dict()
            data_temp[ data['name']] = 'img'+(5-len(str(recipe)))*'0'+str(recipe)+'.jpg'
            ls.append(data_temp)
    return render_template('kitchen.html',img_name = filename,data =ls)

@app.route('/recipe')
def recipe():
    return render_template('list.html')

if __name__ == '__main__':
  app.run(host='127.0.0.1', port=8000, debug=True)
 