from flask import Flask, jsonify, render_template, request, session
from game_logic import PartitaBriscola

app = Flask(__name__)
app.secret_key = "chiave_segreta_briscola_multiplayer"

partita = PartitaBriscola()


@app.route("/")
def home():
  # Assegna il ruolo (1 o 2) in base all'ordine di arrivo nella sessione
  if "ruolo" not in session:
    if partita.giocatori_connessi == 0:
      session["ruolo"] = 1
      partita.giocatori_connessi += 1
    elif partita.giocatori_connessi == 1:
      session["ruolo"] = 2
      partita.giocatori_connessi += 1
    else:
      session["ruolo"] = 0  # Spettatore se la stanza è piena

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


if __name__ == "__main__":
  app.run()
        
    return jsonify(partita.to_dict())

if __name__ == "__main__":
    app.run()
