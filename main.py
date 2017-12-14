from flask import Flask, request, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:demo@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
#app.secret_key = 'y337kGcys&zP3B'


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(240))
    body = db.Column(db.String(2400))

    def __init__(title, content):
        self.title = title
        self.body = body


@app.route('/blog', methods=['GET'])
def blog():
    return render_template('blog.html')


@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']

        if len(title) == 0 or len(body) == 0:
            flash('Must input Title and Content', 'error')
        else:
            return redirect('/blog?id=')

    return render_template('newpost.html', title=title, body=body)


@app.route('/')
def index():
    return redirect('/')


if __name__ == '__main__':
    app.run()
