from flask import Flask, request, redirect, url_for
import os
import jinja2
import re

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)

app = Flask(__name__)
app.config['DEBUG'] = True
posts=[["heading1","text1ext1",0],["heading2","text2 text2",1]] #posts -- list of all posts (for debugging only)
@app.route("/")
def index():
    template = jinja_env.get_template('error_login_form.html')
    return template.render()

def get_post(number):
    global posts
    if number == "all":
        return posts
    elif number >= 0 and number < len(posts):
        return posts[number]
    else:
        return ["error_index","error"]

def add_post(mytitle, mytext):
    global posts
    
    posts.append([mytitle, mytext, len(posts)])

# The main page
@app.route("/blog")
def blog():
    template = jinja_env.get_template('blog_tmpl.html')
    post_list = get_post('all')
    return template.render(post_list=post_list)

@app.route("/newpost")
def newpost():
    template = jinja_env.get_template('newpost_tmpl.html')
    return template.render()

@app.route("/newpost", methods=['POST'])
def form_post():
    title = request.form['title']
    maintext = request.form['maintext']
    add_post(title, maintext)
    template = jinja_env.get_template('singl_post_tmpl.html')
    return template.render(tmpl_title=title, maintext=maintext)
    

@app.route('/post')
def show_post():
    id = int(request.args.get("id"))
    title = get_post(id)[0]
    maintext = get_post(id)[1]
    template = jinja_env.get_template('singl_post_tmpl.html')
    return template.render(tmpl_title=title, maintext=maintext)


app.run()