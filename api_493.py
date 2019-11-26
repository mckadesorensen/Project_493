import html
import json

from flask import Flask, render_template
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

# Probably should delete this to make it less secure
app.config['SECRET_KEY'] = 'bea161e19046d27c00575859500b7dd0'
# Temp posts
posts = [
    {
        "account" :"McKade Sorensen",
        "tweet" : "@ChenyiLing How are you doing?",
        "date_posted" : "10/5/2019"
    },
    {
        "account" :"Chenyi Ling",
        "tweet" : "@McKadeSorensen Great",
        "date_posted" : "10/6/2019"
    }
]


@app.route("/")
@app.route("/home")
def home() -> html:
    return render_template('home.html', posts=posts)


@app.route("/about")
def about() -> html:
    return render_template('about.html', title="About")


@app.route("/register", methods=['GET', 'POST'])
def register() -> None:
    form = RegistrationForm()
    return render_template('register.html', title="Register", form=form)


@app.route("/login")
def login() -> None:
    form = LoginForm()
    return render_template('login.html', title="Login", form=form)


if __name__ == "__main__":
    app.run(debug=True)
