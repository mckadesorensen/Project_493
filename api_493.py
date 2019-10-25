import html

from flask import Flask, render_template

app = Flask(__name__)

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






if __name__ == "__main__":
    app.run(debug=True)
