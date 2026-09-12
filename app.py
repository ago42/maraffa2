from flask import Flask, render_template, jsonify, request
from game_logic import PartitaBriscola

app = Flask(__name__)
partita = PartitaBriscola()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/stato", methods=["GET"])
def get_stato():
    return jsonify(partita.to_dict())

@app.route("/api/scegli-briscola", methods=["POST"])
def scegli_briscola():
    seme = request.json.get("seme")
    partita.imposta_briscola(seme)
    return jsonify(partita.to_dict())

@app.route("/api/gioca-turno", methods=["POST"])
def gioca_turno():
    c1 = request.json.get("carta1")
    c2 = request.json.get("carta2")
    partita.gioca_turno(c1, c2)
    
    if partita.fase == "FINITA":
        p1, p2 = partita.calcola_punteggio_finale()
        return jsonify({"stato": partita.to_dict(), "punti_g1": p1, "punti_g2": p2})
        
    return jsonify(partita.to_dict())

if __name__ == "__main__":
    app.run()
