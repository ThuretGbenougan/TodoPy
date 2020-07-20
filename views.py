from flask import Flask, redirect, url_for, render_template, request, flash,session
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "les"
app.permanent_session_lifetime = timedelta(minutes=5)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///do.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['WTF_CSRF_ENABLED'] = True

db = SQLAlchemy(app)

class Doing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    status=db.Column(db.Boolean,default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, name,user_id ):
        self.name = name
        self.user_id =user_id
    
    def __repr__(self):
        return '<name %s>' %self.name
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    doing = db.relationship('Doing',backref='user')

    def __init__(self, username):
        self.username = username
    
    def __repr__(self):
        return '<username %s>' %self.username


db.create_all()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/view/<int:id>" , methods=["POST", "GET"])
def view(id):
    if "id" in session:
        task=Doing.query.filter_by(user_id=id)
        return render_template("view.html",values=task)
    return redirect(url_for('login'))

@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        session.permanent_session_lifetime = True
        
        username = request.form["username"]
        name_ = User(username=username)

        db.session.add(name_)
        db.session.commit()
        
        return redirect(url_for('login'))
           
    else:
        return render_template("register.html")
        

@app.route('/delete/<int:id>')
def delete(id):
    task_delete = Doing.query.get_or_404(id)
    db.session.delete(task_delete)
    db.session.commit()
    return redirect(url_for('view',id=session['id']))

@app.route('/done/<int:id>')
def done(id):
    task_fait = Doing.query.get(id)
    task_fait.status=True
    db.session.commit()
    return redirect(url_for('view',id=session['id']))

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task_edit = Doing.query.get_or_404(id)
    db.session.delete(task_edit)

    if request.method == 'POST':
        task = request.form['tache']
        task_ = Doing(task,session['id'])
        db.session.add(task_)
        db.session.commit()
        return redirect(url_for('view',id=session['id']))
    else:
        return render_template('maj.html', task=task_edit)
 
@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent_session_lifetime = True
        username = request.form["username"]
        user = User.query.filter_by(username=username).first_or_404()
        session["id"]=user.id
        return redirect(url_for("view",id=user.id))
    else:
        return render_template("login.html")


@app.route("/task/", methods=["POST", "GET"])
def task():
    
    if request.method == "POST":
        name = request.form["name"]
        name_ = Doing(name,session['id'])
        db.session.add(name_)
        db.session.commit()
        return redirect(url_for('view',id=session['id']))
    else:
        return render_template("addtask.html")


@app.route("/userr")
def userr():
    if "userr" in session:
        userr = session["userr"]
        # return f"<h1>{userr}</h1>"
        return redirect(url_for('view'))
    else:
        return redirect(url_for('login'))

@app.route("/profile")
def profile():
    if "userr" in session:

        # tasker=User.query.all()
        tasker=Doing.query.filter_by(user_id=1).first()  
        return render_template("profile.html",values=tasker)
    return redirect(url_for('login'))
    
@app.route("/logout")
def logout():
    session.pop("userr", None)
    return redirect(url_for("login"))
        
# @app.route("/<email>")
# def email(email):
#     return f"<h1>{email}</h1>"

if __name__ == "__main__":
    db.create_all
    app.run(debug=True)