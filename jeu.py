"""Interface terminal du lot 3 : affichage de l'état du moteur."""

from moteur import nouvelle_partie


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


if __name__ == "__main__":
    afficher_grille(nouvelle_partie())
