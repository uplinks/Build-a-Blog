from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy 


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:password@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'thisissecret'


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(8000))

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/blog', methods=['POST', 'GET'])
def index():

    single_id = request.args.get("id")
    if single_id:
        blog = Blog.query.filter_by(id=single_id).first()
        return render_template("single_post.html", blog=blog)
    else:
        blogs = Blog.query.all()
        return render_template('index.html', title="Grr", blogs=blogs)

@app.route('/newpost', methods=['POST', 'GET'])
def new_post():

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        if len(title) == 0 and len(body) == 0:
            flash("Both can not be empty", 'error')
            return render_template('new_post.html')        
        elif len(title) == 0:
            flash('Title can not be empty', 'error')
            return render_template('new_post.html', body=body)
        elif len(body) == 0:
            flash('Body can not be empty', 'error')
            return render_template('new_post.html', title=title)

        else:

            new_entry = Blog(title, body)
            db.session.add(new_entry)
            db.session.commit()

            single_id = new_entry.id
            return redirect("/blog?id={0}".format(single_id))

    return render_template('new_post.html')

if __name__ == '__main__':
    app.run()