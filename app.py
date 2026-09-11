from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Server del gioco di carte online attivo!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)