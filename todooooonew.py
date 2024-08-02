from flask import*
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/mytodo_db'
app.secret_key = 'key'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    

with app.app_context():
    db.create_all()


@app.route('/', methods=['GET','POST'])

@app.route('/<int:todo_id>',methods=['GET','POST'])
def index(todo_id=None):
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')  # Get the description from the form
        if todo_id is None:
            todo = Todo(title=title, description=description)
            db.session.add(todo)
            db.session.commit()
            flash('Todo item added successfully','success')
        else:
            todo = Todo.query.get(todo_id)
            if todo:
                todo.title = title
                todo.description = description  # Update the description
                db.session.commit()
                flash('Todo item updated successfully','success')

        return redirect(url_for('index'))

    todo = None
    if todo_id is not None:
        todo = Todo.query.get(todo_id)
    todos= Todo.query.order_by(Todo.id.desc()).all()
    
    return render_template('todoindex.html',todos= todos,todo=todo)


@app.route('/todo-delete/<int:todo_id>',methods=["POST"])
def delete(todo_id):
    todo = Todo.query.get(todo_id)
    if todo:
        db.session.delete(todo)
        db.session.commit()
        flash('Todo item deleted successfully','success')
    
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)

