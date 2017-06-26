from flask import Flask, request, redirect, url_for
import os
import jinja2
import re

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)

app = Flask(__name__)
app.config['DEBUG'] = True
posts=[["heading1","text1ext1"],["heading2","text2 text2"]] #posts -- list of all posts (for debugging only)
@app.route("/")
def index():
    template = jinja_env.get_template('error_login_form.html')
    return template.render()

def get_post(number):
    global posts
    if number == "all":
        return posts
   # elif number >= 0 and number < len(posts):
    else:
        return posts[number]
  #  else:
    #    return ["error_index","error"]

def add_post(mytitle, mytext):
    global posts
    
    posts.append([mytitle, mytext])

# The main page
@app.route("/blog")
def blog():
    template = jinja_env.get_template('blog_tmpl.html')
    post_list = get_post('all')
    return template.render(post_list=post_list)

@app.route("/newpost")
def newpost():
    template = jinja_env.get_template('newpost_tmpl.html')
    #main_url = url_for("blog")
    #add_np_url = url_for("newpost")
    return template.render()

@app.route("/newpost", methods=['POST'])
def form_post():
    title = request.form['title']
    maintext = request.form['maintext']
    add_post(title, maintext)
    return redirect('/blog')

@app.route('/post')
def show_post():
    id = int(request.args.get("error"))
    title = get_post(id)[0]
    maintext = get_post(id)[1]
    template = jinja_env.get_template('singl_post_tmpl.html')
    return template.render(tmpl_title=title, maintext=maintext)

    
@app.route("/login", methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    verefypassword = request.form['verefypassword']
    email = request.form['email']
    username_error = check_username(username)
    password_error = check_password(password, verefypassword)
    email_error = check_email(email)
    if not username_error and not password_error and not email_error:
        return redirect('/valid-login?login='+username)
    else:
        template = jinja_env.get_template('error_login_form.html')
        if len(password_error) != '':
            password = ''
            verefypassword = ''
        return template.render(user_error=username_error, password_error=password_error,
                               eml_error=email_error, username=username,
                               password=password, verefypassword=verefypassword, email=email)

def check_username(un):
    if re.match("^[a-zA-Z0-9]+$", un) is not None and len(un) > 2:
        return ''
    else:
        return 'Error: only alphanumeric is allowed, with length>2'
def check_password(pwd, vpwd):
    error_msg = ''
    if (re.match("^[a-zA-Z0-9]+$", pwd) is None):
        error_msg = error_msg + 'only alphanumeric is allowed,'
    if len(pwd) <= 7:
        error_msg = error_msg + ' your password is too short,'
    if pwd != vpwd:
        error_msg = error_msg + " you entered different passwords"
    return error_msg

def check_email(eml):
    if (re.match("^[a-zA-Z0-9@.]+$", eml) is not None \
                and len(eml) > 3 \
                and re.search("[@]", eml) is not None) or eml == '':
        return ''
    else:
        return 'Error: it is not valid e-mail address'  

@app.route('/valid-login')
def valid_time():
    uname = request.args.get('login')
    template = jinja_env.get_template('Welcome.html')
    return template.render(name=uname)

app.run()