from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///network.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(15))


class Post(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    title = db.Column(db.String(50), nullable = False)
    content = db.Column(db.Text())
    date = db.Column(db.DateTime(), default = datetime.utcnow)

    def __repr__(self):
        return f'post if: {self.id}, its title: {self.title}, date: {self.date}'


@app.route("/")
def index():
    # post1 = Post(id = 2, title = 'My second post')
    # db.session.add(post1)
    # db.session.commit()
    posts = Post.query.all()
    #return f'{posts}'
    return render_template('posts.html', posts = posts)
    #return redirect(url_for("post"))


@app.route("/create_post/", methods=['GET', 'POST'])
def create_post():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        post = Post(title=title, content=content)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('createpost.html')

with app.app_context():
    db.create_all()

app.run(debug=True, port=5000)