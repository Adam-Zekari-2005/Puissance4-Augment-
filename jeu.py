"""Interface terminal du lot 3 : partie à deux joueurs au clavier."""

from moteur import activer_regles, coups_possibles, gagnant, jouer, nouvelle_partie
from regles import REGLES, decrire_evenements


def afficher_grille(etat):
    """Affiche l'état sans le modifier, avec la ligne 0 en haut."""
    print("  " + " ".join(str(c) for c in range(etat["colonnes"])))
    for ligne in etat["grille"]:
        print("| " + " ".join("." if case is None else case for case in ligne) + " |")
    print("Légende : . vide, X et O joueurs, G jeton gris")
    if etat["fini"]:
        print("Partie terminée.")
    else:
        print(f"Tour {etat['tour']} — au joueur {etat['joueur']} de jouer.")


def saisir_coup(etat):
    """Redemande un entier jusqu'à obtenir un coup autorisé par le moteur."""
    autorises = coups_possibles(etat)
    print("Coups possibles : " + ", ".join(str(coup) for coup in autorises))
    while True:
        try:
            coup = int(input("Votre coup : "))
        except ValueError:
            print("Saisie incorrecte. Entrez un nombre entier.")
            continue
        if coup in autorises:
            return coup
        print("Coup interdit. Choisissez un des coups possibles.")


def lancer_partie():
    """Active les cinq règles et joue jusqu'à la victoire ou au match nul."""
    activer_regles(REGLES)
    etat = nouvelle_partie()
    print("Puissance 4 augmenté — deux joueurs")
    print("Pose : 0 à 6. Pop out : -1 pour la colonne 0, jusqu'à -7 pour la colonne 6.")
    afficher_grille(etat)

    while not etat["fini"]:
        try:
            coup = saisir_coup(etat)
        except (EOFError, KeyboardInterrupt):
            print("\nPartie interrompue.")
            return
        try:
            nouvel_etat = jouer(etat, coup)
        except ValueError:
            print("Coup refusé par le moteur. Recommencez.")
            continue
        for message in decrire_evenements(etat, coup, nouvel_etat):
            print(message)
        etat = nouvel_etat
        afficher_grille(etat)

    resultat = gagnant(etat)
    if resultat == "nul":
        print("Match nul.")
    else:
        print(f"Le joueur {resultat} gagne !")


if __name__ == "__main__":
    lancer_partie()
