"""Tests des 5 regles maison, tires de REGLEMENT-v1.md.

Lancement :  python test_reglement.py
Chaque cas = une suite de coups (Pop out en colonne c note -(c+1)) et le
resultat annonce par le reglement. Les tests du socle restent dans test_socle.py.
"""

import sys

import moteur as M
from regles import REGLES

resultats = []


def cas(nom):
    def decorateur(fn):
        try:
            M.activer_regles(REGLES)
            fn()
            resultats.append((True, nom, ""))
        except AssertionError as e:
            resultats.append((False, nom, str(e) or "assertion"))
        except Exception as e:
            resultats.append((False, nom, f"{type(e).__name__}: {e}"))
        finally:
            M.activer_regles(None)
        return fn
    return decorateur


def R(coups):
    return M.rejouer(coups, REGLES)


def refuse(coups, coup):
    e = R(coups)
    try:
        M.jouer(e, coup)
    except ValueError:
        return
    raise AssertionError(f"le coup {coup} aurait du etre refuse")


BAS = 5

# --- Exemples de reference du reglement ---------------------------------------

@cas("R1 Pop out : [0,0,-1] -> le O descend, au tour de O")
def _():
    e = R([0, 0, -1])
    assert e["grille"][BAS][0] == "O" and e["grille"][BAS - 1][0] is None
    assert e["joueur"] == "O" and M.gagnant(e) is None


@cas("R1 Pop out : retirer un jeton adverse est refuse")
def _():
    refuse([0], -1)


@cas("R1 Pop out : retirer dans une colonne vide est refuse")
def _():
    refuse([], -4)


@cas("R1 + victoire : un Pop out fait gagner l'adversaire")
def _():
    assert M.gagnant(R([0, 0, 1, 1, 3, 2, 3, 2, 6, 3, -4])) == "O"


SUITE15 = [0, 0, 0, 0, 0, 0, 6, 6, 6, 6, 6, 6, 2, 2, 2]


@cas("R2 Gris : apres le 15e coup, gris en ligne 5, colonne 1")
def _():
    e = R(SUITE15)
    assert e["grille"][BAS][1] == "G" and M.gagnant(e) is None
    assert e["coups"] == SUITE15, "le gris ne doit pas entrer dans coups"


@cas("R2 Gris : pas de gris avant le 15e coup")
def _():
    e = R(SUITE15[:14])
    assert all(case != "G" for ligne in e["grille"] for case in ligne)


@cas("R2 + R1 : un gris ne peut pas etre retire")
def _():
    refuse(SUITE15, -2)


@cas("R2 Gris : colonne 1 pleine -> le gris va en colonne 3")
def _():
    e = R([1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 6, 6, 6])
    assert e["grille"][BAS][3] == "G"


GRIS30 = [3, 3, 4, 3, 1, 2, -2, -3, 3, 6, -5, -7, -4, -4, 5, 0, 4, -1, -6, 4,
          -5, -5, 2, -4, 3, 0, -3, -1, -4, 6]


@cas("R2 Gris : le 2e gris (apres le coup 30) vise la colonne 3")
def _():
    e = R(GRIS30)
    assert not e["fini"] and any(ligne[3] == "G" for ligne in e["grille"])


@cas("R3 Carre : [0,6,1,6,0,5,1] -> X gagne")
def _():
    assert M.gagnant(R([0, 6, 1, 6, 0, 5, 1])) == "X"


@cas("R4 Trop aligne : 5 X en ligne -> X perd, O gagne")
def _():
    assert M.gagnant(R([0, 0, 1, 1, 3, 3, 4, 4, 2])) == "O"


@cas("R5 Sandwich : X X O X X -> X gagne")
def _():
    assert M.gagnant(R([0, 2, 1, 6, 3, 6, 4])) == "X"


@cas("R5 + pose : X pose au centre de O O _ O O -> O gagne")
def _():
    assert M.gagnant(R([6, 0, 6, 1, 5, 3, 6, 4, 2])) == "O"


# --- Interactions et cas limites ----------------------------------------------

@cas("Double victoire apres un Pop out -> nul")
def _():
    e = R([3, 3, 0, 4, 2, 5, -4, -4, 1, 2, 0, -6, -2, 0, -1, 1, 4, -5, -5, 0, -3, 5,
           6, 6, -1, 4, 3, -6, 2, 4, -7, 0, 0, -1, 6, 3, 5, 2, 1, 4, 4, 1, 3, -3, 5,
           -5, 2, 4, 4, 5, 6, -5, -4])
    assert M.gagnant(e) == "nul" and e["fini"]


@cas("Double victoire apres une pose (sandwich adverse) -> nul")
def _():
    e = R([5, 3, -6, 2, 4, -3, -5, -4, 4, 2, 3, 2, 5, 5, -6, -3, -5, 4, 3, 4, 3, 0,
           -4, 4, -4, 2, 1, -6, 2, 2, 4, -3, 4, -5, 2, -5, -4, 0, 4, -5, -5, 2, -5,
           1, -5, 4, 2, -1, 4, 1, 5, -3, -3, 6, 4, 3])
    assert M.gagnant(e) == "nul"


@cas("Grille pleine mais Pop out possible -> la partie continue")
def _():
    e = R([4, 0, 0, 6, 4, 3, 0, 3, 2, 1, 0, 0, 3, 1, 3, 2, 0, 2, 3, 2, 5, 3, 2, 4, 2,
           5, 1, 1, 6, 4, 5, 1, 4, 5, 4, 6, 5, 6, 6, 6])
    assert all(case is not None for case in e["grille"][0])
    assert not e["fini"] and M.gagnant(e) is None
    assert M.coups_possibles(e) and all(c < 0 for c in M.coups_possibles(e))


@cas("Limite : nul au coup n 84")
def _():
    coups = GRIS30 + [-4, -7, 3, 5, 4, -6, -5, 2, 0, -3, 3, 2, -1, -3, 2, 2, 6, 3, -7, 5,
                      5, 4, -3, -3, 2, -5, -3, 0, 6, -1, -7, 0, 5, -1, 2, 5, 4, 5, -5, 0,
                      -3, 2, 6, -3, -7, -1, 4, 2, -5, -3, 4, 6, 2, -7]
    e = R(coups)
    assert len(e["coups"]) == 84 and M.gagnant(e) == "nul" and e["fini"]
    assert M.gagnant(R(coups[:83])) is None


@cas("Partie finie : tout coup est refuse")
def _():
    refuse([0, 6, 1, 6, 0, 5, 1], 3)


@cas("Immutabilite avec les regles (pose, Pop out, gris)")
def _():
    for coups, coup in (([0, 0], 3), ([0, 0], -1), (SUITE15[:14], 2)):
        e = R(coups)
        avant = repr(e)
        M.jouer(e, coup)
        assert repr(e) == avant, f"etat modifie par le coup {coup}"


@cas("rejouer avec regles = suite de jouer")
def _():
    coups = [0, 0, -1, 3, 3, -4]
    a = R(coups)
    b = M.nouvelle_partie()
    for c in coups:
        b = M.jouer(b, c)
    assert a == b


@cas("Sans regles : Puissance 4 standard (5 alignes gagne, pas de Pop out)")
def _():
    M.activer_regles(None)
    assert M.gagnant(M.rejouer([0, 0, 1, 1, 3, 3, 4, 4, 2])) == "X"
    try:
        M.jouer(M.rejouer([0]), -1)
    except ValueError:
        return
    raise AssertionError("sans regles, le Pop out doit etre refuse")


reussis = sum(1 for ok, _, _ in resultats if ok)
for ok, nom, detail in resultats:
    print(f"  {'OK  ' if ok else 'ECHEC'} {nom}{'' if ok else '  -> ' + detail}")
print(f"\n{reussis}/{len(resultats)} tests du reglement passent")
sys.exit(0 if reussis == len(resultats) else 1)
