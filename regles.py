"""Les cinq regles maison (lot 2), branchees sur les hooks de moteur.py.

Chaque regle est un dictionnaire qui fournit les hooks ou elle se declenche
(voir REGLEMENT-v1.md, « Ordre d'application general »). Aucune ne modifie
l'etat recu.

Utilisation :  from regles import REGLES ;  moteur.rejouer(coups, REGLES)
"""

from moteur import plus_long_alignement


def _copie(etat):
    copie = dict(etat)
    copie["grille"] = [ligne[:] for ligne in etat["grille"]]
    copie["coups"] = list(etat["coups"])
    return copie


def _adversaire(joueur):
    return "O" if joueur == "X" else "X"


# --- Regle 1 — Pop out --------------------------------------------------------

def _r1_avant_coup(etat, coups):
    """Ajoute -(c+1) pour chaque colonne dont le jeton du bas est au joueur."""
    bas = etat["grille"][etat["lignes"] - 1]
    retraits = [-(c + 1) for c in range(etat["colonnes"]) if bas[c] == etat["joueur"]]
    return coups + retraits


def _r1_pendant_coup(etat, coup):
    """Retire le jeton du bas et fait descendre la pile d'une case."""
    if coup >= 0:
        return None
    c = -coup - 1
    nouvel = _copie(etat)
    g = nouvel["grille"]
    for l in range(nouvel["lignes"] - 1, 0, -1):
        g[l][c] = g[l - 1][c]
    g[0][c] = None
    return nouvel


def _r1_nul(etat):
    """Nul au coup n° 2 x colonnes x lignes ; grille pleine nulle seulement
    si le joueur dont c'est le tour ne peut rien retirer."""
    if len(etat["coups"]) >= 2 * etat["colonnes"] * etat["lignes"]:
        return True
    if all(case is not None for case in etat["grille"][0]):
        return etat["joueur"] not in etat["grille"][etat["lignes"] - 1]
    return None


R1_POP_OUT = {
    "nom": "R1 Pop out",
    "avant_coup": _r1_avant_coup,
    "pendant_coup": _r1_pendant_coup,
    "nul": _r1_nul,
}


# --- Regle 2 — Jeton gris -----------------------------------------------------

SEQUENCE_GRIS = (1, 3, 5)  # 2e, 4e et 6e colonnes


def _r2_fin_de_tour(etat):
    n = len(etat["coups"])
    if n == 0 or n % 15 != 0:
        return etat
    seq = [c for c in SEQUENCE_GRIS if c < etat["colonnes"]]
    if not seq:
        return etat
    k = n // 15                      # k-ieme gris prevu
    depart = (k - 1) % len(seq)
    for i in range(len(seq)):
        c = seq[(depart + i) % len(seq)]
        if etat["grille"][0][c] is None:      # colonne non pleine
            nouvel = _copie(etat)
            for l in range(nouvel["lignes"] - 1, -1, -1):
                if nouvel["grille"][l][c] is None:
                    nouvel["grille"][l][c] = "G"
                    return nouvel
    return etat                       # 1, 3 et 5 pleines : pas de gris


R2_JETON_GRIS = {"nom": "R2 Jeton gris", "fin_de_tour": _r2_fin_de_tour}


# --- Regle 3 — Carre ----------------------------------------------------------

def _r3_apres_coup(etat, joueur):
    g = etat["grille"]
    for l in range(etat["lignes"] - 1):
        for c in range(etat["colonnes"] - 1):
            if g[l][c] == g[l][c + 1] == g[l + 1][c] == g[l + 1][c + 1] == joueur:
                return {"gagne": True}
    return {"gagne": False}


R3_CARRE = {"nom": "R3 Carre", "apres_coup": _r3_apres_coup}


# --- Regle 4 — Trop aligne ----------------------------------------------------

def _r4_apres_coup(etat, joueur):
    return {"perd": plus_long_alignement(etat["grille"], joueur) >= 5}


R4_TROP_ALIGNE = {"nom": "R4 Trop aligne", "apres_coup": _r4_apres_coup}


# --- Regle 5 — Sandwich horizontal --------------------------------------------

def _r5_apres_coup(etat, joueur):
    motif = [joueur, joueur, _adversaire(joueur), joueur, joueur]
    for ligne in etat["grille"]:
        for c in range(etat["colonnes"] - 4):
            if ligne[c:c + 5] == motif:
                return {"gagne": True}
    return {"gagne": False}


R5_SANDWICH = {"nom": "R5 Sandwich", "apres_coup": _r5_apres_coup}


# Ordre d'application a l'interieur d'un meme hook : R1 -> R5.
REGLES = [R1_POP_OUT, R2_JETON_GRIS, R3_CARRE, R4_TROP_ALIGNE, R5_SANDWICH]
