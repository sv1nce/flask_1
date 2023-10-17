from flask import Flask, request,redirect,render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask_1.db'
db = SQLAlchemy(app)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    
    
    

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/add', methods= ['POST', 'GET'])
def add():
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']
        
        post = Post(title = title,text = text)
        
        try:
            db.session.add(post)
            db.session.commit()
            return redirect('/')
        except:
            return f'While adding a post there was a mistake'
    else:
        return render_template('add.html')
    
@app.route('/posts')
def posts():
    posts = Post.query.all()
    return render_template('posts.html', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html')
   
if __name__ == '__main__':
    app.run(debug=True)