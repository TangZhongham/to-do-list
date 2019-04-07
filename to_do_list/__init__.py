from flask import Flask
from flask_script import Manager
from flask_bootstrap import Bootstrap


app = Flask(__name__)
app.config["SECRET_KEY"] = "my_precious"

bootstrap = Bootstrap(app)
manager = Manager(app)

from to_do_list import views
