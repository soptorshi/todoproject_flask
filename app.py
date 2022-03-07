from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    # completed = db.Column(db.Boolean)
    completed = db.Column(db.String(20),nullable = False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow() )

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/', methods=['POST','GET'])
def entry_page():
    return render_template('entry_page.html')

@app.route('/login/', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
    else:
        return render_template('login.html')

@app.route('/register/',methods = ['POST','GET'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
    else:
        return render_template('register.html')


@app.route('/home/', methods = ['POST','GET']) 
def index():
    if request.method == 'POST':
        content = request.form['content']
        completed = request.form['completed']
        new_task = Todo(content = content, completed = completed)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/home/')
        except:
            return 'Error!'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks = tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/home/')
    except:
        return 'Error!'

@app.route('/update/<int:id>', methods= ['POST','GET'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']
        task.completed = request.form['completed']
        try:
            db.session.commit()
            return redirect('/home/')
        except:
            return 'Error!'
    else:
        return render_template('update.html',task = task)

if __name__ == '__main__':
    app.run(debug=True)