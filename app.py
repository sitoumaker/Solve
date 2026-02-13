from flask import Flask, render_template, request
import itertools
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DICT_PATH = os.path.join(BASE_DIR, "mots.txt")

@app.route("/", methods=["GET", "POST"])
def solve():
    resultat = []
    erreur = None

    if request.method == "POST":
        lettres = request.form.get("text", "").lower().strip()
        k = request.form.get("number", "").strip()

        if not lettres.isalpha() :
            erreur = "Entrée invalide : lettres incorrect."
        else:
            b = int(k)

            if b < 0:
                erreur = "Sérieusement un nombre négatif !"

            elif b > len(lettres) or b > 7:
                erreur = "Nombre trop grand par rapport aux lettres."

            else:
                with open(DICT_PATH, encoding="utf-8") as f:
                    dico = {ligne.strip().lower() for ligne in f if ligne.strip()}

                solutions = set()

                for p in itertools.permutations(lettres, b):
                    mot = ''.join(p)
                    if mot in dico:
                        solutions.add(mot)

                if not solutions:
                    erreur = "Aucun mot correspondant trouvé."
                else:
                    resultat = sorted(solutions)

    return render_template("solve.html", resultat=resultat, erreur=erreur)


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run()
