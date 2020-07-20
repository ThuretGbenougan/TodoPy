from flask import Flask, redirect, url_for, render_template, request, flash,session
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "les"
app.permanent_session_lifetime = timedelta(minutes=5)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///do.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

class Doing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    status=db.Column(db.Boolean,default=False)

    def __init__(self, name):
        self.name = name
    
    def __repr(self):
        return '<name %s>' %self.name



db.create_all()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/view" , methods=["POST", "GET"])
def view():
    if "userr" in session:
        userr = session["userr"]
        task=Doing.query.all()  
        return render_template("view.html",values=task)
    else:
        flash("Connectez vous d'abord!", "info  ")
        return redirect('/login')
        

@app.route('/delete/<int:id>')
def delete(id):
    task_delete = Doing.query.get_or_404(id)
    db.session.delete(task_delete)
    db.session.commit()
    return redirect('/view')

@app.route('/done/<int:id>')
def done(id):
    task_fait = Doing.query.get(id)
    task_fait.status=True
    db.session.commit()
    return redirect('/view')

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task_edit = Doing.query.get_or_404(id)
    db.session.delete(task_edit)

    if request.method == 'POST':
        email = request.form['email']
        email_ = Doing(name=email)
        db.session.add(email_)
        db.session.commit()
        return redirect('/view')
       
    else:
        return render_template('maj.html', task=task_edit)

    
@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent_session_lifetime = True
        user = request.form["names"]
        session["user"]=userr
        return redirect(url_for("userr"))
    else:
        if "userr" in session:
            return redirect(url_for("userr"))
        return render_template("login.html")

@app.route("/task", methods=["POST", "GET"])
def task():
    if request.method == "POST":
        name = request.form["name"]
        name_ = Doing(name=name)

        db.session.add(name_)
        db.session.commit()
        
        return redirect('/view')
           
        # return redirect(url_for("email", email=email))
    else:
        return render_template("addtask.html")


@app.route("/userr",methods=["POST", "GET"])
def userr():
    if "userr" in session:
        userr = session["userr"]
        return f"<h1>{userr}</h1>"
    else:
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