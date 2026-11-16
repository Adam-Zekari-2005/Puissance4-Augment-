"""Interface terminal du lot 3 : une partie complete au clavier, cinq regles actives.

L'interface ne connait aucune regle : elle affiche un etat, lit un coup, le fait
valider par coups_possibles() et l'execute par jouer(). La fin de partie vient de
gagnant(). Les messages des regles viennent de regles.decrire_coup().

Lancer :  python jeu.py
"""

from moteur import activer_regles, coups_possibles, gagnant, jouer, nouvelle_partie
from regles import REGLES, decrire_coup

AIDE = """Commandes :
  0 a 6      poser un jeton dans cette colonne
  r0 a r6    Pop out : retirer son propre jeton du bas de cette colonne
  aide       afficher cette aide
  q          quitter"""


def afficher_grille(etat):
    """Affiche l'etat sans le modifier, avec la ligne 0 en haut."""
    print()
    print("  " + " ".join(str(c) for c in range(etat["colonnes"])))
    for ligne in etat["grille"]:
        print("| " + " ".join("." if case is None else case for case in ligne) + " |")
    print("Legende : . vide, X et O joueurs, G jeton gris")
    if etat["fini"]:
        print("Partie terminee.")
    else:
        print(f"Tour {etat['tour']} — au joueur {etat['joueur']} de jouer.")


def nom_du_coup(coup):
    """Texte lisible d'un coup du contrat : c >= 0 pose, -(c+1) retire en c."""
    return f"r{-coup - 1}" if coup < 0 else str(coup)


def lire_coup(texte):
    """Traduit la saisie en coup du contrat (entier), ou leve ValueError."""
    texte = texte.strip().lower()
    retrait = texte.startswith("r")
    if retrait:
        texte = texte[1:].strip()
    if not texte.isdigit():
        raise ValueError("saisie non reconnue")
    colonne = int(texte)
    return -(colonne + 1) if retrait else colonne


def annoncer_fin(etat):
    resultat = gagnant(etat)
    if resultat == "nul":
        print("Resultat : match nul.")
    else:
        print(f"Resultat : {resultat} gagne.")
    print("Coups joues : [" + ", ".join(str(c) for c in etat["coups"]) + "]")


def partie(lire=input):
    """Joue une partie complete. `lire` permet de simuler le clavier."""
    activer_regles(REGLES)          # toujours les cinq regles (voir AGENTS.md)
    etat = nouvelle_partie()
    print("Puissance 4 augmente — cinq regles maison actives.")
    print(AIDE)
    while not etat["fini"]:
        afficher_grille(etat)
        possibles = coups_possibles(etat)
        print("Coups possibles : " + " ".join(nom_du_coup(c) for c in possibles))
        saisie = lire(f"{etat['joueur']} > ")
        if saisie.strip().lower() in ("q", "quit", "quitter"):
            print("Partie abandonnee.")
            return etat
        if saisie.strip().lower() in ("aide", "h", "?"):
            print(AIDE)
            continue
        try:
            coup = lire_coup(saisie)
        except ValueError:
            print("Saisie refusee : tapez un numero de colonne (0 a 6) ou r suivi "
                  "d'un numero pour un Pop out.")
            continue
        if coup not in possibles:
            print(f"Coup refuse : {nom_du_coup(coup)} n'est pas autorise maintenant.")
            continue
        try:
            nouvel = jouer(etat, coup)
        except ValueError as erreur:
            print(f"Coup refuse par le moteur : {erreur}")
            continue
        for message in decrire_coup(etat, nouvel):
            print("  >> " + message)
        etat = nouvel
    afficher_grille(etat)
    annoncer_fin(etat)
    return etat


if __name__ == "__main__":
    try:
        partie()
    except (EOFError, KeyboardInterrupt):
        print("\nPartie interrompue.")
