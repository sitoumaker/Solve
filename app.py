from flask import Flask, render_template, request
import itertools
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DICT_PATH = os.path.join(BASE_DIR, "mots.txt")

@app.route("/", methods=["GET", "POST"])
def solve():
    resultat = []

    if request.method == "POST":
        lettres = request.form.get("text", "").lower()
        k = request.form.get("number", "")

        # Vérifications
        if lettres.isalpha() and k.isdigit():
            b = int(k)

            # Sécurité : éviter explosion de calcul
            if b > len(lettres) or b > 7:
                resultat = ["Entrée trop grande"]
            else:
                with open(DICT_PATH, encoding="utf-8") as f:
                    dico = {ligne.strip().lower() for ligne in f if ligne.strip()}

                solutions = set()

                for p in itertools.permutations(lettres, b):
                    mot = ''.join(p)
                    if mot in dico:
                        solutions.add(mot)

                resultat = sorted(solutions)
        else:
            resultat = ["Entrée invalide"]

    return render_template("solve.html", resultat=resultat)


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run()
