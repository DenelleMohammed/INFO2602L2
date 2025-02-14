import click, sys
from models import db, User, Todo
from app import app
from sqlalchemy.exc import IntegrityError

#creating a command "init" to be run from the terminal
@app.cli.command("init", help="Creates and initializes the database")
def initialize():
  db.drop_all()
  db.init_app(app)
  db.create_all()
  bob = User('bob', 'bob@mail.com', 'bobpass')
  bob.todos.append(Todo('wash car'))
  db.session.add(bob)
  db.session.commit()
  print(bob)
  print('database intialized')
  #adding information to the database
  db.session.add(bob) 
  db.session.commit()
  print(bob)

@app.cli.command("get-user", help="Retrieves a User")
@click.argument('username', default='bob')
def get_user(username):
  bob = User.query.filter_by(username=username).first()
  if not bob:
    print(f'{username} not found!')
    return
  print(bob)

@app.cli.command('get-users')
def get_users():
  # gets all objects of a model
  users = User.query.all()
  print(users)

@app.cli.command("change-email")
@click.argument('username', default='bob')
@click.argument('email', default='bob@mail.com')
def change_email(username, email):
  bob = User.query.filter_by(username=username).first()
  if not bob:
      print(f'{username} not found!')
      return
  bob.email = email
  db.session.add(bob)
  db.session.commit()
  print(bob)

@app.cli.command('create-user')
@click.argument('username', default='rick')
@click.argument('email', default='rick@mail.com')
@click.argument('password', default='rickpass')
def create_user(username, email, password):
  newuser = User(username, email, password)
  try:
    db.session.add(newuser)
    db.session.commit()
  except IntegrityError as e:
    #let's the database undo any previous steps of a transaction
    db.session.rollback()
    # print(e.orig) #optionally print the error raised by the database
    print("Username or email already taken!") #give the user a useful message
  else:
    print(newuser) # print the newly created user

@app.cli.command('delete-user')
@click.argument('username', default='bob')
def delete_user(username):
  bob = User.query.filter_by(username=username).first()
  if not bob:
      print(f'{username} not found!')
      return
  db.session.delete(bob)
  db.session.commit()
  print(f'{username} deleted')

@app.cli.command('get-todos')
@click.argument('username', default='bob')
def get_user_todos(username):
  bob = User.query.filter_by(username=username).first()
  if not bob:
      print(f'{username} not found!')
      return
  print(bob.todos)

@app.cli.command('add-todo')
@click.argument('username', default='bob')
@click.argument('text', default='wash car')
def add_task(username, text):
  bob = User.query.filter_by(username=username).first()
  if not bob:
      print(f'{username} not found!')
      return
  new_todo = Todo(text)
  bob.todos.append(new_todo)
  db.session.add(bob)
  db.session.commit()

@click.argument('todo_id', default=1)
@click.argument('username', default='bob')
@app.cli.command('toggle-todo')
def toggle_todo_command(todo_id, username):
  user = User.query.filter_by(username=username).first()
  if not user:
    print(f'{username} not found!')
    return

  todo = Todo.query.filter_by(id=todo_id, user_id=user.id).first()
  if not todo:
    print(f'{username} has no todo id {todo_id}')

  todo.toggle()
  print(f'{todo.text} is {"done" if todo.done else "not done"}!')

@click.argument('username', default='bob')
@click.argument('todo_id', default=6)
@click.argument('category', default='chores')
@app.cli.command('add-category', help="Adds a category to a todo")
def add_todo_category_command(username, todo_id, category):
  user = User.query.filter_by(username=username).first()
  if not user:
    print(f'{username} not found!')
    return

  res = user.add_todo_category(todo_id, category)
  if not res:
    print(f'{username} has no todo id {todo_id}')
    return

  print('Category added!')