from flask import Flask, render_template
app = Flask(__name__)
@app.route('/home')
def home():
    return "My nama jeff"

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/hello/<name>')
def say_hello(name):
    return "Hello there, {}".format(name)
