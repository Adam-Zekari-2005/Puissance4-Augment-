# Puissance 4 augmenté

## Contexte et sources
- Projet universitaire : Puissance 4 en Python, interface terminal, cinq règles originales. Le professeur évalue surtout la précision des spécifications et leur vérification.
- Fin de séance 2 ; séance 3 non commencée. Codex est l'agent principal, Claude Code prend le relais si nécessaire. L'utilisation de Codex est autorisée par le professeur selon l'utilisateur.
- Consignes de référence : les PDF « Puissance 4 augmenté — Séance 1.pdf », « Puissance 4 augmenté — Séance 2.pdf » et « Puissance 4 augmenté — Séance 3.pdf ».
- Règlement de référence : `REGLEMENT-v1 (1).md` (nom réel). Le lire avant toute tâche liée aux règles ; ne pas le recopier ici ni inventer les informations manquantes.

## Méthode demandée par l'utilisateur
- Une tâche à la fois. Avant chaque modification, expliquer brièvement le changement prévu et attendre la validation ; rester dans le périmètre approuvé.
- Ne pas développer toute une séance d'un coup. Ne pas modifier le règlement v1 sans autorisation ; le PDF demande de conserver la v1 remise et de rendre les évolutions dans des versions distinctes.
- Répondre en français, simplement et brièvement. Signaler les ambiguïtés avant de choisir un comportement.

## Contrat du moteur
Préserver les noms et paramètres :
```python
nouvelle_partie(colonnes=7, lignes=6)
coups_possibles(etat)
jouer(etat, colonne)
gagnant(etat)
rejouer(coups, regles=None)
```
L'état est un dictionnaire : `colonnes`, `lignes`, `grille` (listes de lignes, `None` pour une case vide), `joueur` (`X` commence, puis `O`), `tour` (initialement 1), `coups` (initialement vide), `fini` (initialement `False`). Ligne 0 en haut ; colonnes 0 à 6 sur la grille standard 7 × 6.

- Aucun changement de la forme imposée de l'état, aucune bibliothèque externe pour le moteur. `jouer()` renvoie un nouvel état sans modifier celui reçu ; un coup illégal lève `ValueError`.
- `gagnant()` renvoie `X`, `O`, `nul` ou `None`. Préserver les 16 tests du socle standard : `python -B test_socle.py moteur` (`-B` évite les caches).
- Les règles maison appartiennent à `regles.py` et se branchent sur un point d'accroche ; elles ne doivent pas être dispersées dans les fonctions standard.

## Décisions déjà inscrites dans le règlement
- Quatre moments : `AVANT_COUP`, `PENDANT_COUP`, `APRES_COUP`, `FIN_DE_TOUR`. Le règlement définit les déclenchements et priorités exacts.
- Une règle reçoit l'état sans le modifier : autorisation avant le coup, nouvel état pendant le coup ou en fin de tour, indications de victoire/défaite après le coup. Les deux joueurs sont évalués selon le tableau de priorités du règlement.
- Aucune règle à usage limité ; le calendrier des jetons gris se déduit de `len(coups)`. Les retraits sont encodés `-(colonne+1)` dans l'historique. La même suite de coups doit reproduire le même état.

## État vérifié et reprise
- `moteur.py` contient le jeu standard ; `test_socle.py` a passé 16/16 tests lors de l'analyse précédente. Ce résultat ne valide pas les règles maison et doit être revérifié après une modification pertinente.
- Le règlement décrit les points d'accroche, mais leur branchement n'est pas développé ; `rejouer()` ignore actuellement son argument `regles`.
- À la création de ce document : `regles.py`, `jeu.py`, `RECETTE.md`, `QUESTIONS.md`, `ECHECS.md` et `sessions/` sont absents. La validation professorale des règles et l'attribution nominative des lots ne sont pas attestées dans les fichiers.
- Avant de développer une règle : vérifier sa validation par l'enseignant et écrire ses résultats attendus dans `RECETTE.md`. Une règle, une vérification, puis consignation de l'observé. Objectif final : 20 à 30 cas, au moins deux par règle et un par interaction déclarée, avec les cas limites.
- Documenter les décisions et les résultats réellement obtenus au fil du travail. `QUESTIONS.md` reçoit les réponses aux questions du professeur ; `ECHECS.md` décrit trois échecs réels de l'IA (demande, résultat, détection, correction de la demande). Ne rien fabriquer ni antidater.
- Conserver les journaux bruts individuels dans `sessions/<prénom>/`, sans retouche. Ne pas supposer qu'un agent les y exporte automatiquement. Pour chaque tâche autorisée, laisser une trace concise des changements, tests et points ouverts afin de permettre la reprise.
- La prochaine tâche reste soumise à validation de l'utilisateur ; ne pas commencer la séance 3 automatiquement.
