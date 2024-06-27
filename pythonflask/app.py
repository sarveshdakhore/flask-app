from flask import Flask, request, render_template
import datetime
import psycopg2
import database
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField
from wtforms.validators import DataRequired




app = Flask(__name__)
app.config['SECRET_KEY']="anykey"

class Signupform(FlaskForm):
   name=StringField("Whats your name", validators=[DataRequired()])
   email=StringField("Whats your email", validators=[DataRequired()])
   phone=StringField("Whats your phone no")
   password=PasswordField("Whats your password", validators=[DataRequired()])

   submit=SubmitField("submit")

class LoginForm(FlaskForm):
   email=StringField("Whats your email or phone no", validators=[DataRequired()])
   password=PasswordField("Whats your password", validators=[DataRequired()])

   submit=SubmitField("submit")


@app.route("/")
def main_page():
  return render_template("index.html")

@app.route("/new_user", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        dt=datetime.datetime.now()
        name=None
        email=None
        phone=None
        password=None
        status=''
        form=Signupform()
        if form.validate_on_submit():
            name=form.name.data
            email=form.email.data
            phone=form.phone.data
            password=form.password.data
            form.name.data=" "
            print("--------------------------------------------------- name:\n ", name)
            status= database.insert(name, email,phone,password,dt)



    return render_template("signup.html", name=name,email=email,phone=phone,password=password,form=form,status=status)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email=None
        password=None
        status=''
        loginform=LoginForm()
        print(loginform.validate_on_submit())
        if loginform.validate_on_submit():
            email=loginform.email.data
            password=loginform.password.data
            
            status= database.fetch(email,password)

        else:
    # Access validation errors
          for field, errors in loginform.errors.items():
              print(f"Error in field {field}: {errors}")
        if status=="Data feteched successfully!":
          return render_template("login.html",email=email,password=password,task="/tasks",form=loginform)
        else:
           return render_template("login.html",email=email,password=password,status=status,form=loginform)
        
    return render_template("login.html",email=email,password=password,form=loginform)

@app.route("/tasks", methods=["GET", "POST"])
def tasks_page():
  print("taskspage")
  return render_template("tasks.html")




if __name__=='__main__':
  app.run(debug=True)
