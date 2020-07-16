from flask import Flask, redirect, url_for, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
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
    task=Doing.query.all()  
    return render_template("view.html",values=task)

@app.route('/delete/<int:id>')
def delete(id):
    task_delete = Doing.query.get_or_404(id)

    db.session.delete(task_delete)
    db.session.commit()
    return redirect('/view')

@app.route('/fait/<int:id>')
def fait(id):
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
        userr = request.form["nm"]
       
        return redirect(url_for("userr", usr=userr))
    else:
        return render_template("login.html")

@app.route("/user", methods=["POST", "GET"])
def user():
    if request.method == "POST":
        email = request.form["email"]
        email_ = Doing(name=email)
    
        db.session.add(email_)
        db.session.commit()
        
        return redirect('/view')
           
        # return redirect(url_for("email", email=email))
    else:
        return render_template("user.html")


@app.route("/<usr>")
def userr(usr):
    return f"<h1>{usr}</h1>"
@app.route("/<email>")
def email(email):
    return f"<h1>{email}</h1>"

if __name__ == "__main__":
    db.create_all
    app.run(debug=True)