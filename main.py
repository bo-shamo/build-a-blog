from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import cgi

app = Flask(__name__)
app.config['DEBUG'] = True      # displays runtime errors in the browser, too
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:itisablog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(512))
    deleted = db.Column(db.Boolean)
    
    def __init__(self):
        self.deleted = False



@app.route('/blog' , methods=['GET'])
@app.route('/', methods=['GET'])
def index():

    posts = Blog.query.filter_by(deleted=False).all()    
    return render_template('blog.html', blog = posts)

@app.route('/newpost')
def add_blog():
    new_blog = Blog()
    db.session.add(new_blog)
    db.session.commit()

    return render_template("newpost.html", blog = new_blog)

@app.route('/addblog', methods=['POST'])
def confirm_add_blog():
    blog_id = int(request.form['blog-id'])
    blog = Blog.query.get(blog_id)
    blog.title = request.form['title']
    blog.body = request.form['body']
    error = ""
    #error handling if any of the boxes are empty
    if blog.title == "":
        error = "Please add a title"
    elif blog.body == "":
        error = "Please add a body"

    if error != "":
        return render_template("newpost.html", blog=blog, error = error)
    else:
        db.session.add(blog)
        db.session.commit()
        return redirect('/blog')

@app.route('/ind-blog')
def individual_blog():
    blog_id = request.args.get('id')
    blog = Blog.query.get(blog_id)
    return render_template("ind-blog.html", blog = blog)


if __name__ == '__main__':
    app.run()