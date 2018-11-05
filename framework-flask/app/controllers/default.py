# arquivo somente para routes
from app import app


@app.route("/")
def index():
    return "I am your father"