from flask import Flask

app = Flask(__name__)
app.config["SECRET_KEY"] = "my_precious"

from to_do_list import views
