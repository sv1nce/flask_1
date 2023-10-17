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
            return redirect('/posts')
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

@app.route('/post/<int:post_id>')
def view_post(post_id):
    post = Post.query.get(post_id)
    if post :
        return render_template('post.html', post=post)
    else:
        return "Post not found", 404

@app.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    post = Post.query.get(post_id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.text = request.form['text']
        try:
            db.session.commit()
            return redirect ('/posts')
        except:
            return 'An error occurred while editing the post'
    return render_template('edit_post.html', post=post)

@app.route('/delete_post/<int:post_id>')
def delete_post(post_id):
    post = Post.query.get(post_id)
    try:
        db.session.delete(post)
        db.session.commit()
        return redirect('/posts')
    except:
        return 'An error occurred while deleting the post'
       
if __name__ == '__main__':
    app.run(debug=True)