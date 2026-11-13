"""Puissance 4 — socle impose. Lot 1.

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

# Regles maison actives (liste de dictionnaires de hooks, voir regles.py).
# Vide = Puissance 4 standard : c'est ce que verifie test_socle.py.
REGLES_ACTIVES = []


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
    """Indices des colonnes ou l'on peut encore jouer, dans l'ordre croissant.

    Renvoie une liste vide si la partie est finie.
    Avec des regles actives, le hook AVANT_COUP peut ajouter des coups
    (Regle 1 : les Pop out, codes -(c+1), ajoutes apres les colonnes).
    """
    if etat["fini"]:
        return []
    coups = [c for c in range(etat["colonnes"]) if etat["grille"][0][c] is None]
    for regle in REGLES_ACTIVES:  # hook AVANT_COUP
        if "avant_coup" in regle:
            coups = regle["avant_coup"](etat, coups)
    return coups


def jouer(etat, colonne):
    """Joue un jeton dans `colonne` et renvoie un NOUVEL etat.

    L'etat recu ne doit pas etre modifie — c'est ce qui permet de rejouer une partie
    et de revenir en arriere. Leve ValueError si le coup est illegal.
    """
    # Hook 1 — AVANT_COUP : le coup est-il autorise ?
    if isinstance(colonne, bool) or not isinstance(colonne, int) \
            or colonne not in coups_possibles(etat):
        raise ValueError(f"coup illegal : {colonne!r}")

    base = _copie(etat)

    # Hook 2 — PENDANT_COUP : execution (la premiere regle qui prend le coup en
    # charge l'emporte, sinon pose standard par gravite).
    nouvel = None
    for regle in REGLES_ACTIVES:
        if "pendant_coup" in regle:
            nouvel = regle["pendant_coup"](base, colonne)
            if nouvel is not None:
                break
    if nouvel is None:
        nouvel = _poser(base, colonne, etat["joueur"])

    nouvel["coups"] = etat["coups"] + [colonne]
    nouvel["tour"] = etat["tour"] + 1
    nouvel["joueur"] = _adversaire(etat["joueur"])  # change apres CHAQUE coup accepte

    # Hook 3 — APRES_COUP : la partie est-elle finie (victoire / defaite) ?
    if _resultat_victoire(nouvel) is not None:
        nouvel["fini"] = True
        return nouvel

    # Hook 4 — FIN_DE_TOUR : la main est passee ; evenements automatiques (gris).
    for regle in REGLES_ACTIVES:
        if "fin_de_tour" in regle:
            nouvel = regle["fin_de_tour"](nouvel)

    # ... puis match nul.
    nouvel["fini"] = _resultat_nul(nouvel) is not None
    return nouvel


def gagnant(etat):
    """'X', 'O', 'nul' si la grille est pleine sans alignement, sinon None."""
    resultat = _resultat_victoire(etat)
    if resultat is not None:
        return resultat
    return _resultat_nul(etat)


def rejouer(coups, regles=None):
    """Rejoue une partie entiere depuis une liste de colonnes. Deja ecrit.

    C'est par cette fonction que votre jeu sera verifie : elle doit rester capable
    de rejouer n'importe quelle suite de coups, regles maison comprises.
    Sans `regles`, c'est le Puissance 4 standard.
    """
    activer_regles(regles)
    etat = nouvelle_partie()
    for colonne in coups:
        etat = jouer(etat, colonne)
    return etat


def activer_regles(regles=None):
    """Choisit les regles maison actives (None ou [] = Puissance 4 standard)."""
    global REGLES_ACTIVES
    REGLES_ACTIVES = list(regles or [])


# ---------------------------------------------------------------------------
# Outils internes du moteur (ne font pas partie du contrat)
# ---------------------------------------------------------------------------

def _adversaire(joueur):
    return "O" if joueur == "X" else "X"


def _copie(etat):
    """Copie complete de l'etat : la grille est recopiee ligne par ligne."""
    copie = dict(etat)
    copie["grille"] = [ligne[:] for ligne in etat["grille"]]
    copie["coups"] = list(etat["coups"])
    return copie


def _poser(etat, colonne, jeton):
    """Pose `jeton` par gravite dans `colonne` d'un etat DEJA copie, et le renvoie."""
    for ligne in range(etat["lignes"] - 1, -1, -1):
        if etat["grille"][ligne][colonne] is None:
            etat["grille"][ligne][colonne] = jeton
            return etat
    raise ValueError(f"colonne {colonne} pleine")


def plus_long_alignement(grille, joueur):
    """Longueur du plus long alignement de `joueur` (4 directions)."""
    lignes, colonnes = len(grille), len(grille[0])
    meilleur = 0
    for l in range(lignes):
        for c in range(colonnes):
            if grille[l][c] != joueur:
                continue
            for dl, dc in ((0, 1), (1, 0), (1, 1), (-1, 1)):
                pl, pc = l - dl, c - dc
                if 0 <= pl < lignes and 0 <= pc < colonnes and grille[pl][pc] == joueur:
                    continue  # pas le debut de cet alignement
                n, ll, cc = 0, l, c
                while 0 <= ll < lignes and 0 <= cc < colonnes and grille[ll][cc] == joueur:
                    n, ll, cc = n + 1, ll + dl, cc + dc
                meilleur = max(meilleur, n)
    return meilleur


def _resultat_victoire(etat):
    """Hook 3 — APRES_COUP. 'X', 'O', 'nul' ou None.

    Base : 'gagne' si alignement de 4 ou plus. Les regles ajoutent 'gagne' ou
    'perd' ; le tableau de priorites du reglement tranche.
    """
    if not etat["coups"]:
        return None
    a = _adversaire(etat["joueur"])  # le joueur qui vient de jouer
    b = etat["joueur"]
    avis = {}
    for joueur in (a, b):
        gagne = plus_long_alignement(etat["grille"], joueur) >= 4
        perd = False
        for regle in REGLES_ACTIVES:
            if "apres_coup" in regle:
                r = regle["apres_coup"](etat, joueur)
                gagne = gagne or r.get("gagne", False)
                perd = perd or r.get("perd", False)
        avis[joueur] = (gagne, perd)
    (ga, pa), (gb, pb) = avis[a], avis[b]
    if pa and pb:
        return "nul"   # priorite 1
    if pa:
        return b       # priorite 2
    if pb:
        return a       # priorite 3
    if ga and gb:
        return "nul"   # priorite 4
    if ga:
        return a       # priorite 5
    if gb:
        return b       # priorite 6
    return None


def _resultat_nul(etat):
    """Hook 4 — FIN_DE_TOUR, partie match nul. 'nul' ou None.

    Base : nul si la grille est pleine. Une regle peut forcer (True) ou
    empecher (False) le nul ; None = pas d'avis.
    """
    nul = all(case is not None for case in etat["grille"][0])
    for regle in REGLES_ACTIVES:
        if "nul" in regle:
            avis = regle["nul"](etat)
            if avis is not None:
                nul = avis
    return "nul" if nul else None


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
# -> Reponses du groupe (detail dans CLAUDE.md et REGLEMENT-v1.md) :
#
#   - Quand ? A l'un des 4 hooks d'un coup. Une regle est un dict qui fournit
#     les cles des hooks ou elle se declenche :
#       "avant_coup"(etat, coups)   -> liste des coups autorises    (AVANT_COUP)
#       "pendant_coup"(etat, coup)  -> nouvel etat ou None          (PENDANT_COUP)
#       "apres_coup"(etat, joueur)  -> {"gagne": bool, "perd": bool} (APRES_COUP)
#       "fin_de_tour"(etat)         -> nouvel etat                  (FIN_DE_TOUR)
#       "nul"(etat)                 -> True / False / None          (FIN_DE_TOUR)
#   - Recoit / rend : l'etat recu n'est JAMAIS modifie ; une regle rend un nouvel
#     etat ou une reponse simple.
#   - Ordre : hooks 1 -> 4, puis ordre de la liste des regles (R1 -> R5) ; la
#     victoire est tranchee par le tableau de priorites (_resultat_victoire).
#   - Usage limite : dans l'etat. Aucune de nos regles n'en a besoin : tout se
#     deduit de len(coups) et de la grille.
#
# Activation : rejouer(coups, regles) ou activer_regles(regles).
