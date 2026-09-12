js_content = """let cartaSelezionataG1 = null;
let cartaSelezionataG2 = null;
let statoAttuale = null;

// Carica lo stato iniziale all'avvio
document.addEventListener("DOMContentLoaded", () => {
    aggiornaStato();
});

async function aggiornaStato() {
    try {
        const response = await fetch('/api/stato');
        statoAttuale = await response.json();
        renderizzaGioco(statoAttuale);
    } catch (err) {
        console.error("Errore nel recupero dello stato:", err);
    }
}

function renderizzaGioco(stato) {
    // 1. Gestione Modal Briscola
    const modalBriscola = document.getElementById('modal-briscola');
    if (!stato.briscole) {
        modalBriscola.classList.remove('hidden');
    } else {
        modalBriscola.classList.add('hidden');
        document.getElementById('briscola-attuale').textContent = stato.briscole;
    }

    // 2. Info Turno e Carte Rimaste
    document.getElementById('turno-attuale').textContent = `Giocatore ${stato.prio}`;
    document.getElementById('carte-rimaste').textContent = stato.carte_rimaste_mazzo;

    // 3. Renderizza Mano Giocatore 1
    const containerG1 = document.getElementById('mano-g1');
    containerG1.innerHTML = '';
    stato.mano_g1.forEach(cartaStr => {
        const cardElem = creaElementoCarta(cartaStr, (c) => selezionaCarta(c, 1));
        if (cartaSelezionataG1 === cartaStr) {
            cardElem.classList.add('selezionata');
        }
        containerG1.appendChild(cardElem);
    });

    // 4. Renderizza Mano Giocatore 2
    const containerG2 = document.getElementById('mano-g2');
    containerG2.innerHTML = '';
    stato.mano_g2.forEach(cartaStr => {
        // Mostriamo carte visibili per test/interfaccia locale, oppure coperte
        const cardElem = creaElementoCarta(cartaStr, (c) => selezionaCarta(c, 2));
        if (cartaSelezionataG2 === cartaStr) {
            cardElem.classList.add('selezionata');
        }
        containerG2.appendChild(cardElem);
    });

    // 5. Abilita/Disabilita Bottone Gioca
    const btnGioca = document.getElementById('btn-conferma-turno');
    btnGioca.disabled = !(cartaSelezionataG1 && cartaSelezionataG2);

    // 6. Controlla Fine Partita
    if (stato.fase === "FINITA") {
        mostraFinePartita();
    }
}

function creaElementoCarta(cartaStr, onClickHandler) {
    const parts = cartaStr.split(' ');
    const seme = parts[0];
    const valore = parts[1];

    const card = document.createElement('div');
    card.className = 'carta';
    card.onclick = () => onClickHandler(cartaStr);

    const iconaSeme = {
        'Denari': '♦',
        'Coppe': '🍷',
        'Spade': '⚔',
        'Bastoni': '🪵'
    }[seme] || '';

    card.innerHTML = `
        <div class="valore-carta">${valore}</div>
        <div class="seme-carta">${iconaSeme}</div>
        <div class="valore-carta" style="align-self: flex-end;">${seme}</div>
    `;

    return card;
}

function selezionaCarta(cartaStr, giocatore) {
    if (giocatore === 1) {
        cartaSelezionataG1 = (cartaSelezionataG1 === cartaStr) ? null : cartaStr;
    } else {
        cartaSelezionataG2 = (cartaSelezionataG2 === cartaStr) ? null : cartaStr;
    }
    renderizzaGioco(statoAttuale);
}

async function scegliBriscola(seme) {
    try {
        const res = await fetch('/api/scegli-briscola', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ seme: seme })
        });
        const nuovoStato = await res.json();
        statoAttuale = nuovoStato;
        renderizzaGioco(statoAttuale);
    } catch (err) {
        console.error("Errore nella selezione della briscola:", err);
    }
}

async function inviaGiocata() {
    if (!cartaSelezionataG1 || !cartaSelezionataG2) return;

    try {
        const res = await fetch('/api/gioca-turno', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                carta1: cartaSelezionataG1,
                carta2: cartaSelezionataG2
            })
        });

        const risp = await res.json();
        
        // Aggiorna gli slot in campo visivamente
        document.getElementById('slot-g1').innerHTML = '';
        document.getElementById('slot-g1').appendChild(creaElementoCarta(cartaSelezionataG1, ()=>{}));
        
        document.getElementById('slot-g2').innerHTML = '';
        document.getElementById('slot-g2').appendChild(creaElementoCarta(cartaSelezionataG2, ()=>{}));

        // Reset selezioni
        cartaSelezionataG1 = null;
        cartaSelezionataG2 = null;

        if (risp.punti_g1 !== undefined) {
            mostraFinePartita(risp.punti_g1, risp.punti_g2);
        } else {
            statoAttuale = risp;
            renderizzaGioco(statoAttuale);
        }

    } catch (err) {
        console.error("Errore nell'invio della giocata:", err);
    }
}

function mostraFinePartita(p1, p2) {
    const modalFine = document.getElementById('modal-fine');
    const punteggioBox = document.getElementById('esito-punteggio');
    punteggioBox.innerHTML = `<p>Giocatore 1: <strong>${p1}</strong> punti</p><p>Giocatore 2: <strong>${p2}</strong> punti</p>`;
    modalFine.classList.remove('hidden');
}

function nuovaPartita() {
    location.reload();
}
"""

with open("templates/index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

with open("static/css/style.css", "w", encoding="utf-8") as f:
    f.write(css_content)

with open("static/js/main.js", "w", encoding="utf-8") as f:
    f.write(js_content)

print("File dell'interfaccia grafica creati con successo!")