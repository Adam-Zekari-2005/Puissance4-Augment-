"""Interface terminal : deux joueurs, adversaire aléatoire et outils de rejeu."""

import json
import random

from moteur import activer_regles, coups_possibles, gagnant, jouer, nouvelle_partie, rejouer
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
        saisie = input("Votre coup (h : historique) : ").strip()
        if saisie.lower() == "h":
            afficher_historique(etat)
            continue
        try:
            coup = int(saisie)
        except ValueError:
            print("Saisie incorrecte. Entrez un nombre entier.")
            continue
        if coup in autorises:
            return coup
        print("Coup interdit. Choisissez un des coups possibles.")


def afficher_historique(etat):
    """Liste copiable telle quelle dans le mode rejeu, retraits compris."""
    print("Historique des coups :")
    print(etat["coups"])


def afficher_resultat(etat):
    resultat = gagnant(etat)
    if resultat == "nul":
        print("Match nul.")
    elif resultat is not None:
        print(f"Le joueur {resultat} gagne !")
    else:
        print("Partie en cours.")


def lire_historique(texte):
    """Accepte une liste d'entiers sans exécuter la saisie comme du code."""
    try:
        coups = json.loads(texte)
    except (ValueError, RecursionError):
        raise ValueError("Entrez une liste comme [0, 0, -1].") from None
    if not isinstance(coups, list) or any(type(c) is not int for c in coups):
        raise ValueError("La liste doit contenir uniquement des entiers.")
    return coups


def rejouer_depuis_terminal():
    while True:
        texte = input("Liste des coups (ou q pour revenir) : ").strip()
        if texte.lower() == "q":
            return
        try:
            coups = lire_historique(texte)
            etat = rejouer(coups, REGLES)
        except ValueError as erreur:
            print(f"Rejeu refusé : {erreur}")
            continue
        afficher_grille(etat)
        afficher_resultat(etat)
        afficher_historique(etat)
        return etat


def lancer_partie(ordinateur=False):
    """Active les cinq règles et joue jusqu'à la victoire ou au match nul."""
    activer_regles(REGLES)
    etat = nouvelle_partie()
    print("Puissance 4 augmenté — " + (
        "vous jouez X, l'ordinateur joue O" if ordinateur else "deux joueurs"
    ))
    print("Pose : 0 à 6. Pop out : -1 pour la colonne 0, jusqu'à -7 pour la colonne 6.")
    afficher_grille(etat)

    while not etat["fini"]:
        try:
            if ordinateur and etat["joueur"] == "O":
                coup = random.choice(coups_possibles(etat))
                print(f"L'ordinateur joue : {coup}")
            else:
                coup = saisir_coup(etat)
        except (EOFError, KeyboardInterrupt):
            print("\nPartie interrompue.")
            afficher_historique(etat)
            return etat
        try:
            nouvel_etat = jouer(etat, coup)
        except ValueError:
            print("Coup refusé par le moteur. Recommencez.")
            continue
        for message in decrire_evenements(etat, coup, nouvel_etat):
            print(message)
        etat = nouvel_etat
        afficher_grille(etat)

    afficher_resultat(etat)
    afficher_historique(etat)
    return etat


def menu():
    try:
        while True:
            print("\n1 — Deux joueurs\n2 — Contre l'ordinateur\n3 — Rejouer une liste de coups\nq — Quitter")
            choix = input("Votre choix : ").strip().lower()
            if choix == "q":
                return
            if choix in ("1", "2"):
                lancer_partie(ordinateur=choix == "2")
            elif choix == "3":
                rejouer_depuis_terminal()
            else:
                print("Choisissez 1, 2, 3 ou q.")
    except (EOFError, KeyboardInterrupt):
        print("\nAu revoir.")


if __name__ == "__main__":
    menu()
