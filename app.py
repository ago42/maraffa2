import uuid
from flask import Flask, jsonify, render_template, request, session
from game_logic import PartitaBriscola

app = Flask(__name__)
app.secret_key = "chiave_segreta_briscola_multiplayer_romagnola"

partita = PartitaBriscola()

# Tracciamento dei giocatori tramite ID univoco
giocatori_attivi = {"G1": None, "G2": None}


@app.route("/")
def home():
    if "user_id" not in session:
        session["user_id"] = str(uuid.uuid4())

    user_id = session["user_id"]

    # Assegnazione ruoli dinamica in base a chi è connesso
    if "ruolo" not in session or session["ruolo"] == 0:
        if giocatori_attivi["G1"] is None or giocatori_attivi["G1"] == user_id:
            giocatori_attivi["G1"] = user_id
            session["ruolo"] = 1
        elif giocatori_attivi["G2"] is None or giocatori_attivi["G2"] == user_id:
            giocatori_attivi["G2"] = user_id
            session["ruolo"] = 2
        else:
            session["ruolo"] = 0

    return render_template("index.html")


@app.route("/api/stato", methods=["GET"])
def get_stato():
    dati = partita.to_dict()
    dati["mio_ruolo"] = session.get("ruolo", 0)
    return jsonify(dati)


@app.route("/api/scegli-briscola", methods=["POST"])
def scegli_briscola():
    seme = request.json.get("seme")
    partita.imposta_briscola(seme)
    return jsonify(partita.to_dict())


@app.route("/api/gioca-carta", methods=["POST"])
def gioca_carta():
    ruolo = session.get("ruolo", 0)
    carta = request.json.get("carta")

    if ruolo in [1, 2] and carta:
        partita.gioca_carta_singola(ruolo, carta)

    dati = partita.to_dict()
    dati["mio_ruolo"] = ruolo
    return jsonify(dati)


@app.route("/api/reset", methods=["POST"])
def reset():
    global giocatori_attivi
    session.clear()
    giocatori_attivi = {"G1": None, "G2": None}
    partita.giocatori_connessi = 0
    partita.reset_partita()
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run()
