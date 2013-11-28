from flask import Flask
from flask import render_template
from flask_cake import Cake
from config_options import get_options

app = Flask(__name__)
app.debug = True
Cake(app)

@app.route("/")
def intro():
  return render_template("intro.html")

@app.route("/config/")
def config():
  config_options = get_options()
  return render_template("config.html")

if __name__ == "__main__":
  app.run()
