from flask import Flask, render_template_string
import csv

spieler_liste = []

with open("Spieler.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        row["vereine"] = row["vereine"].split(";")
        spieler_liste.append(row)
import random
from flask import Flask, render_template_string, request

app = Flask(__name__)

# --- HTML Templates ---
style = """
<style>
    body {
        background-color: #1e1e1e;
        color: white;
        font-family: Arial, sans-serif;
        text-align: center;
        padding-top: 400px;
    }

    h1 {
        font-size: 80px;
        margin-bottom: 40px;
        text-align: center;
    }

    h2 {
        font-size: 900px;
        margin-top: 30px;
    }

    p {
        font-size: 45px;
        line-height: 1.6;
        margin-bottom: 20px;
    }
    

    .btn {
        background-color: #1C9FD7;
        border: none;
        padding: 50px 65px;
        font-size: 45px;
        font-weight: bold;
        color: white;
        border-radius: 30px;
        width: 90%;
        max-width: 400px;
        margin-top: 40px;
        display: inline-block;
        text-decoration: none;
    }

    .card {
        background-color: #2b2b2b;
        padding: 80px;
        border-radius: 30px;
        width: 110%;
        max-width: 600px;
        margin: auto;
        margin-top: 40px;
        text-align: left;
    }
</style>
"""

# --- Startseite ---
@app.route("/")
def home():
    html = f"""
    <html>
    <head>{style}</head>
    <body>
        <h1>⚽ FOOTSTER</h1>

        <div class="card">
            <p>Klicke auf <b>Neue Runde</b>, um zu starten.</p>
        </div>

        <a href="/neue_runde" class="btn">Neue Runde</a>
    </body>
    </html>
    """
    return html

# --- Neue Runde ---
@app.route("/neue_runde")
def neue_runde():
    spieler = random.choice(spieler_liste)

    name = spieler["name"]

    html = f"""
    <html>
    <head>{style}</head>
    <body>
        <h1>🎤 HOST-MODUS</h1>

        <div class="card">
            <p><b>👉 Sag den Spielern NUR den Namen!</b></p><br>
            <h2 style="font-size: 55px; margin-top: 20px;">➡️ {name}</h2>
            <p>Wenn alle den Namen gesehen haben, drücke <b>Spiel starten</b>.</p>
        </div>

        <a href="/spiel_starten?name={name}" class="btn">Spiel starten</a>
    </body>
    </html>
    """
    return html

# --- Spiel starten (Auflösung) ---
@app.route("/spiel_starten")
def spiel_starten():
    import urllib.parse
    name = urllib.parse.unquote(request.args.get("name"))

    # Spieler suchen
    spieler = next(s for s in spieler_liste if s["name"] == name)

    nation = spieler["nationalität"]
    position = spieler["position"]
    vereine = "<br>".join("• " + v for v in spieler["vereine"])

    html = f"""
    <html>
    <head>{style}</head>
    <body>
        <h1>📢 Auflösung</h1>

        <div class="card">
            <p><b>👉 Sag den Spielern NUR den Namen!</b></p><br>
            <h2 style="font-size: 55px; margin-top: 20px;">➡️ {name}</h2>
            <p>Wenn alle den Namen gesehen haben, drücke <b>Spiel starten</b>.</p>
        </div>

        <a href="/" class="btn">Neue Runde</a>
    </body>
    </html>
    """
    return html

if __name__ == "__main__":

    app.run(host="0.0.0.0", port=5000)
