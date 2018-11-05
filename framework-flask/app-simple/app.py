from flask import Flask

# create an instance of the Flask class
app = Flask(__name__)

@app.route("/")
def hello():
    return "I am your father !"

# executing the script
if __name__ == "__main__":
    app.run(debug=True, port=5000)