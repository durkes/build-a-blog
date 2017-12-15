from flask import Flask, request, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:demo@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y737kGcys&zP3B'


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(240))
    body = db.Column(db.String(2400))

    def __init__(self, title, body):
        self.title = title
        self.body = body


@app.route('/blog', methods=['GET'])
def blog():
    id = request.args.get('id')
    if id is not None:
        entry = Blog.query.filter_by(id=id).first()
        return render_template('blog.html', title=entry.title, entry=entry)

    entries = Blog.query.all()
    return render_template('blog.html', title="Build a Blog", entries=entries)


@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    title = ""
    body = ""

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']

        if len(title) == 0 or len(body) == 0:
            flash('Must input Title and Content', 'error')
        else:
            new_entry = Blog(title, body)
            db.session.add(new_entry)
            db.session.commit()
            return redirect('/blog?id=' + str(new_entry.id))

    return render_template('newpost.html', title=title, body=body)


@app.route('/')
def index():
    return redirect('/blog')


if __name__ == '__main__':
    app.run()
