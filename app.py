from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect  # Import this!
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length


from flask import Flask, render_template

# 1. SECRET KEY (Required for CSRF)
app.config['SECRET_KEY'] = 'dev-secret-key-12345'

# 2. CSRF PROTECTION (Fixes the 'csrf_token' is undefined error)
csrf = CSRFProtect(app)

# 3. DATABASE CONFIG
app.config["MYSQL_DATABASE_HOST"] = "localhost"
app.config["MYSQL_DATABASE_USER"] = "root"
app.config["MYSQL_DATABASE_PASSWORD"] = "12345"
app.config["MYSQL_DATABASE_DB"] = "form"   

mysql = MySQL(app)

class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=4, max=25)])
    email = StringField("Email Address", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    submit = SubmitField("signup")

@app.route("/signup", methods=["GET", "POST"])
def register():
    form = RegistrationForm()

    # validate_on_submit() automatically checks if it's a POST request AND checks CSRF
    if form.validate_on_submit():
        name = form.username.data
        email = form.email.data     
        password = form.password.data

        try:
            conn = mysql.connect() 
            cursor = conn.cursor()
            cursor.execute("INSERT INTO user (name, email, password) VALUES (%s, %s, %s)", (name, email, password))
            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for("login"))
        except Exception as e:
            return f"Database Error: {e}"

    return render_template("register.html", form=form)

@app.route("/login")
def login():
    form = LoginForm() 
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data       

        cursor = mysql.connect().cursor()
        cursor.execute("SELECT * FROM user WHERE email = %s AND password = %s", (email, password))
        user = cursor.fetchone()
        cursor.close()  

        if user:
            return redirect(url_for("dashboard"))
        else:
            return "Invalid credentials. Please try again."
app = Flask(__name__)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/')
def services():
    return render_template('services.html')

@app.route('/')
def pricing():
    return render_template('pricing.html')

@app.route('/')
def about ():
    return render_template('about.html')




if __name__ =='__main__':
     app.run(debug=True, port=8000)