"""Tests du SOCLE STANDARD (usage enseignant) — Puissance 4 sans regle maison.

Lancement dans le dossier d'un groupe :   python test_socle.py moteur
Sur l'implementation de reference     :   python test_socle.py moteur_reference

Ces tests ne portent QUE sur le Puissance 4 standard : ils doivent passer chez tous
les groupes, quelles que soient leurs cinq regles.
"""

import importlib
import sys

M = importlib.import_module(sys.argv[1] if len(sys.argv) > 1 else "moteur")

resultats = []


def cas(nom):
    def decorateur(fn):
        try:
            fn()
            resultats.append((True, nom, ""))
        except AssertionError as e:
            resultats.append((False, nom, str(e) or "assertion"))
        except Exception as e:
            resultats.append((False, nom, f"{type(e).__name__}: {e}"))
        return fn

    return decorateur


def grille_de(etat):
    return etat["grille"]


@cas("nouvelle_partie : dimensions et grille vide")
def _():
    e = M.nouvelle_partie()
    assert e["colonnes"] == 7 and e["lignes"] == 6
    assert len(e["grille"]) == 6 and len(e["grille"][0]) == 7
    assert all(case is None for ligne in e["grille"] for case in ligne)
    assert e["joueur"] == "X" and e["tour"] == 1 and e["fini"] is False


@cas("coups_possibles : 7 colonnes sur une grille vide")
def _():
    assert M.coups_possibles(M.nouvelle_partie()) == [0, 1, 2, 3, 4, 5, 6]


@cas("gravite : le premier jeton tombe en bas de la colonne")
def _():
    e = M.jouer(M.nouvelle_partie(), 3)
    assert grille_de(e)[5][3] == "X", "le jeton doit occuper la ligne du bas"
    assert grille_de(e)[4][3] is None


@cas("empilement : le second jeton se pose au-dessus")
def _():
    e = M.jouer(M.jouer(M.nouvelle_partie(), 3), 3)
    assert grille_de(e)[5][3] == "X" and grille_de(e)[4][3] == "O"


@cas("alternance : X puis O puis X")
def _():
    e = M.nouvelle_partie()
    assert e["joueur"] == "X"
    e = M.jouer(e, 0)
    assert e["joueur"] == "O"
    e = M.jouer(e, 1)
    assert e["joueur"] == "X"


@cas("immutabilite : jouer ne modifie pas l'etat recu")
def _():
    depart = M.nouvelle_partie()
    M.jouer(depart, 3)
    assert all(case is None for ligne in depart["grille"] for case in ligne), (
        "jouer doit renvoyer un NOUVEL etat, sans toucher au precedent"
    )
    assert depart["tour"] == 1


@cas("colonne pleine : elle disparait des coups possibles")
def _():
    e = M.nouvelle_partie()
    for _ in range(6):
        e = M.jouer(e, 2)
    assert 2 not in M.coups_possibles(e)


@cas("coup illegal : ValueError")
def _():
    e = M.nouvelle_partie()
    for _ in range(6):
        e = M.jouer(e, 2)
    try:
        M.jouer(e, 2)
    except ValueError:
        return
    raise AssertionError("jouer sur une colonne pleine doit lever ValueError")


@cas("victoire horizontale")
def _():
    assert M.rejouer([0, 0, 1, 1, 2, 2, 3])["grille"] is not None
    assert M.gagnant(M.rejouer([0, 0, 1, 1, 2, 2, 3])) == "X"


@cas("victoire verticale")
def _():
    assert M.gagnant(M.rejouer([3, 4, 3, 4, 3, 4, 3])) == "X"


@cas("victoire diagonale montante")
def _():
    assert M.gagnant(M.rejouer([0, 1, 1, 2, 2, 3, 2, 3, 3, 6, 3])) == "X"


@cas("victoire diagonale descendante")
def _():
    assert M.gagnant(M.rejouer([3, 2, 2, 1, 1, 0, 1, 0, 0, 6, 0])) == "X"


@cas("partie en cours : aucun gagnant")
def _():
    assert M.gagnant(M.rejouer([3, 3, 4, 4])) is None


@cas("match nul : grille pleine sans alignement")
def _():
    e = M.nouvelle_partie(colonnes=3, lignes=1)
    for c in (0, 1, 2):
        e = M.jouer(e, c)
    assert M.gagnant(e) == "nul"


@cas("fin de partie : plus aucun coup possible apres une victoire")
def _():
    e = M.rejouer([3, 4, 3, 4, 3, 4, 3])
    assert e["fini"] is True
    assert M.coups_possibles(e) == []


@cas("rejouer : equivalent a une suite de jouer")
def _():
    coups = [3, 3, 4, 2, 5]
    a = M.rejouer(coups)
    b = M.nouvelle_partie()
    for c in coups:
        b = M.jouer(b, c)
    assert a["grille"] == b["grille"] and a["coups"] == b["coups"]


reussis = sum(1 for ok, _, _ in resultats if ok)
for ok, nom, detail in resultats:
    print(f"  {'OK  ' if ok else 'ECHEC'} {nom}{'' if ok else '  -> ' + detail}")
print(f"\n{reussis}/{len(resultats)} tests du socle passent")
sys.exit(0 if reussis == len(resultats) else 1)
