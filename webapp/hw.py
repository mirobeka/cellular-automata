from flask import Flask
from flask import render_template
from flask_cake import Cake

app = Flask(__name__)
app.debug = True
Cake(app)

@app.route("/")
def intro():
  return render_template("intro.html")

@app.route("/hello/<name>")
@app.route("/hello/")
def hw(name=None):
  return render_template("hello.html", name=name)


if __name__ == "__main__":
  app.run()
