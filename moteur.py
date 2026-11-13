"""Puissance 4 - socle impose. Lot 1.

Ces quatre signatures sont un CONTRAT : ne changez ni les noms, ni les parametres,
ni la forme de l'etat. Elles sont verifiees telles quelles a la correction.

L'etat est un dictionnaire, et rien d'autre (pas de classe, pas d'objet) :

    {
        "colonnes": 7,
        "lignes":   6,
        "grille":   [[None, ...], ...],   # grille[ligne][colonne]
                                          # ligne 0 = HAUT, ligne lignes-1 = BAS
        "joueur":   "X",                  # a qui de jouer
        "tour":     1,                    # commence a 1
        "coups":    [],                   # colonnes jouees, dans l'ordre
        "fini":     False,
    }

Regle du jeu de base : chacun depose a son tour un jeton dans une colonne, le jeton
tombe sur la case libre la plus basse, et le premier qui aligne 4 jetons gagne
(horizontalement, verticalement ou en diagonale).

Vos cinq regles maison ne vont PAS ici : voir la section en fin de fichier.
"""

JOUEURS = ("X", "O")


def nouvelle_partie(colonnes=7, lignes=6):
    """Etat d'une partie qui commence. Deja ecrit : c'est la forme de l'etat."""
    return {
        "colonnes": colonnes,
        "lignes": lignes,
        "grille": [[None] * colonnes for _ in range(lignes)],
        "joueur": "X",
        "tour": 1,
        "coups": [],
        "fini": False,
    }


def coups_possibles(etat):
    """Renvoie les indices des colonnes non pleines."""
    if etat["fini"]:
        return []

    colonnes_libres = []
    for colonne in range(etat["colonnes"]):
        if etat["grille"][0][colonne] is None:
            colonnes_libres.append(colonne)

    return colonnes_libres


def jouer(etat, colonne):
    """Joue un jeton et renvoie un nouvel état sans modifier l'ancien."""
    if type(colonne) is not int or colonne not in coups_possibles(etat):
        raise ValueError("Coup illegal")

    # Copier l'état et les listes pour préserver l'état de départ.
    nouvel_etat = etat.copy()
    nouvel_etat["grille"] = [ligne.copy() for ligne in etat["grille"]]
    nouvel_etat["coups"] = etat["coups"].copy()

    # Chercher la première case libre en partant du bas.
    for ligne in range(etat["lignes"] - 1, -1, -1):
        if nouvel_etat["grille"][ligne][colonne] is None:
            nouvel_etat["grille"][ligne][colonne] = etat["joueur"]
            break

    nouvel_etat["coups"].append(colonne)
    nouvel_etat["tour"] += 1

    if etat["joueur"] == "X":
        nouvel_etat["joueur"] = "O"
    else:
        nouvel_etat["joueur"] = "X"

    nouvel_etat["fini"] = gagnant(nouvel_etat) is not None

    return nouvel_etat


def gagnant(etat):
    """Renvoie 'X', 'O', 'nul', ou None si la partie continue."""
    grille = etat["grille"]
    lignes = etat["lignes"]
    colonnes = etat["colonnes"]

    # Horizontale, verticale et les deux diagonales
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

    for ligne in range(lignes):
        for colonne in range(colonnes):
            pion = grille[ligne][colonne]

            if pion is None:
                continue

            for dl, dc in directions:
                fin_ligne = ligne + 3 * dl
                fin_colonne = colonne + 3 * dc

                if not (0 <= fin_ligne < lignes
                        and 0 <= fin_colonne < colonnes):
                    continue

                aligne = True
                for i in range(1, 4):
                    if grille[ligne + i * dl][colonne + i * dc] != pion:
                        aligne = False
                        break

                if aligne:
                    return pion

    # Sans victoire, une case vide signifie que la partie continue.
    for ligne in grille:
        if None in ligne:
            return None

    return "nul"


def rejouer(coups, regles=None):
    """Rejoue une partie entiere depuis une liste de colonnes. Deja ecrit.

    C'est par cette fonction que votre jeu sera verifie : elle doit rester capable
    de rejouer n'importe quelle suite de coups, regles maison comprises.
    """
    etat = nouvelle_partie()
    for colonne in coups:
        etat = jouer(etat, colonne)
    return etat


# ---------------------------------------------------------------------------
# LE POINT D'ACCROCHE DES REGLES MAISON
# ---------------------------------------------------------------------------
# Vos cinq regles ne s'ecrivent pas dans les fonctions ci-dessus : elles arrivent
# ici, et le lot 2 les branchera. C'est a VOUS de decider comment — et cette
# decision se prend au TP2, avant d'ecrire la moindre regle.
#
# Les questions a trancher, et a consigner dans CLAUDE.md :
#
#   - A quel moment une regle intervient-elle ? Avant le coup (elle l'autorise ou
#     l'interdit) ? Apres (elle deplace des jetons) ? Sur la victoire ?
#   - Une regle recoit quoi, et rend quoi ? Un etat ? Un etat modifie ?
#   - Dans quel ordre s'appliquent deux regles declenchees au meme tour ?
#   - Comment une regle a usage limite retient-elle qu'elle a servi ?
#
# Aucune de ces reponses n'est dans ce fichier, et c'est voulu : c'est le travail
# du lot 1 de la concevoir, et celui du lot 2 de s'en servir sans rien reecrire.