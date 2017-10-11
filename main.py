from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:root@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(120))
    body=db.Column(db.String(800))

    def __init__(self, title, body):
        self.title=title
        self.body=body

@app.route('/')
def index():
    return redirect('/blog')

@app.route('/blog')
def blog():
    blogs = Blog.query.order_by(Blog.id.desc()).all()   
    if request.args:
        id=request.args.get('id')
        title = Blog.query.filter_by(id=id).first().title
        body = Blog.query.filter_by(id=id).first().body
        return render_template('single.html',title=title,body=body)
    else:
        return render_template('blog.html', blogs=blogs)

@app.route('/newpost', methods=['GET', 'POST'])
def add_blog():
    if request.method=='GET':
        return render_template('newpost.html')

    if request.method=='POST':
        title=request.form['title']
        body=request.form['body']
        blog_error=''
    if title=='' or body=='':
        blog_error='Title and/or Body field may not be left empty.'
    if blog_error=='':
        new_blog=Blog(title,body)
        db.session.add(new_blog)
        db.session.commit()
        query_url= './blog?id='+ str(new_blog.id)
        return redirect(query_url)
    else:
        return render_template('newpost.html', error=blog_error, title=title, body=body)

if __name__=='__main__':
    app.run()