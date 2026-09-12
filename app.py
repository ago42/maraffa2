from flask import Flask, render_template, jsonify, request
from game_logic import Partita # Importa la classe principale della tua logica

app = Flask(__name__)

# Creiamo un'istanza della partita
partita = Partita()

@app.route("/")
def home():
    # Carica l'interfaccia principale (templates/index.html)
    return render_template("index.html")

@app.route("/api/stato", methods=["GET"])
def get_stato():
    # Restituisce lo stato corrente della partita in formato JSON
    return jsonify(partita.to_dict())

@app.route("/api/gioca-carta", methods=["POST"])
def gioca_carta():
    data = request.json
    indice = data.get("indice_carta")
    
    # Esegue la mossa usando la tua logica
    esito, messaggio = partita.giocatore_corrente.gioca_carta(indice)
    
    return jsonify({
        "successo": esito,
        "messaggio": messaggio,
        "stato": partita.to_dict()
    })

if __name__ == "__main__":
    app.run(debug=True)
