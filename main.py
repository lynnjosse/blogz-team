from models import User, Blog
from flask import request, redirect, render_template, session, flash
import datetime
from app import app, db
from hashutil import make_pw_hash, check_pw_hash, make_salt

endpoints_without_login = ['login', 'register', 'index', 'main_page']

@app.before_request
def require_login():
    if not ('user' in session or request.endpoint in endpoints_without_login):
        return redirect("/login")

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

        if (not username) or (username.strip() == ""):
            flash("Please enter a username." , 'danger')
            return redirect ('/register')
        if (not password) or (password.strip() == ""):
            flash("Please enter a password.", 'danger')
            return redirect ('/register')   

        if password != verify:
            flash('passwords do not match', 'danger')
            return redirect('/register')

        if len(username)<3 or len(username)>20:
            flash("Valid usernames must have between 3 and 20 characters", 'danger')
            return redirect('/register')

        if len(password)<3 or len(password)>20:
            flash('Valid passwords must have between 3 and 20 characters', 'danger') 
            return redirect('/register')      

        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            user = new_user
            session['user'] = user.username
            
            return redirect('/blog')
        else:
            flash('That username is already in use', 'danger')
            return redirect('/register')
    else:
        return render_template('register.html')     

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = User.query.filter_by(username=username)
        if users.count() == 1:
            user = users.first()
            if check_pw_hash(password, user.pw_hash):
                session['user'] = user.username
                flash('welcome back, '+ user.username, 'success')
                return redirect("/blog")
        flash('bad username or password', 'danger')
        return redirect("/login")  

@app.route("/logout", methods=['POST'])
def logout():
    del session['user']
    return redirect("/blog")                        


@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', title = "Our Contributors", users = users) 

@app.route('/blog', methods=['GET', 'POST'])
def main_page():

    if request.args.get('id'):
        id = int(request.args.get('id'))
        blogs = [Blog.query.get(id)]
    elif request.args.get('owner_id'):
        owner_id = int(request.args.get('owner_id'))
        blogs = Blog.query.filter_by(owner_id=owner_id).all()

    else:
        blogs = Blog.query.all()
    return render_template('blog.html', title = "This Blog", blogs = blogs)

@app.route('/newpost', methods=['GET', 'POST'])
def post_it(): 
    
    title = "New Post"

    return render_template('newpost.html' , title = title)
     
@app.route("/add", methods=['POST'])
def add_post():
    # look inside the request to figure out what the user typed
    new_post_title = request.form['title']
    new_post_body = request.form['blog']
    owner = User.query.filter_by(username= session['user']).first()

    # if the user typed nothing at all, redirect and tell them the error
    if (not new_post_title) or (new_post_title.strip() == ""):
    
        flash("Your post must have a title.")
        return redirect ('/newpost')
        
    if (not new_post_body) or (new_post_body.strip() ==""):
        flash("Your post must have a body.")
        return redirect ('/newpost')

    new_post = Blog(new_post_title, new_post_body, owner)
    db.session.add(new_post)
    db.session.commit()
    
    #find the id of the newly committed object

    current_post = Blog.query.filter_by(title = new_post_title).first()

    id = current_post.id
    
    return redirect ('/blog?id=' + str(id))


if __name__ == '__main__':
    app.run()