# Puissance 4 augmenté

## Contexte et sources
- Projet universitaire : Puissance 4 en Python, interface terminal, cinq règles originales. Le professeur évalue surtout la précision des spécifications et leur vérification.
- Base de fin de séance 2 récupérée sur le PC d'un membre du groupe : elle contient déjà les cinq règles codées. Codex est l'agent principal, Claude Code prend le relais si nécessaire. Son utilisation est autorisée par le professeur selon l'utilisateur.
- Consignes de référence : les PDF « Puissance 4 augmenté — Séance 1.pdf », « Puissance 4 augmenté — Séance 2.pdf » et « Puissance 4 augmenté — Séance 3.pdf ».
- Règlement de référence : `REGLEMENT-v1.md`. Le lire avant toute tâche liée aux règles ; ne pas le recopier ici ni inventer les informations manquantes.

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

## Branchement existant (archive du groupe)
- `regles.py` expose `REGLES`, liste de dictionnaires de fonctions : `avant_coup(etat, coups)` renvoie les coups autorisés ; `pendant_coup(etat, coup)` un nouvel état ou `None` ; `apres_coup(etat, joueur)` les avis `gagne`/`perd` ; `fin_de_tour(etat)` un état ; `nul(etat)` `True`, `False` ou `None`.
- `activer_regles(regles)` définit la variable globale `REGLES_ACTIVES`. `rejouer(coups, regles=None)` active les règles fournies (aucune par défaut). Un seul ensemble est actif : après un changement de mode, réactiver les règles d'une ancienne partie avant de la consulter ou de la poursuivre. Cette limite est documentée dans `SUIVI.md` ; ne pas prétendre que les parties sont isolées. Ne pas ajouter de champ à l'état pour gérer plusieurs modes simultanés, exigence absente des PDF.
- Le code change actuellement le joueur avant la vérification de victoire, y compris au dernier coup ; le règlement situe ce changement en fin de tour. Cet écart reste à clarifier, pas à modifier sans accord.

## État vérifié et reprise
- `moteur.py`, `regles.py` et `test_reglement.py` proviennent de l'archive `Travailler IA.zip`. Le règlement a seulement été renommé ; `test_socle.py` est inchangé.
- Les tests de l'archive ont réussi : 16/16 pour le socle, 21/21 pour les règles. Commande complémentaire : `python -B test_reglement.py`. Ces résultats ne prouvent pas la conformité complète ; les limites et vérifications d'intégration sont dans `SUIVI.md`.
- `jeu.py`, `RECETTE.md`, `QUESTIONS.md`, `ECHECS.md` et `sessions/` restent absents. La validation professorale des règles et l'attribution nominative des lots ne sont pas attestées dans les fichiers.
- Avant de développer une règle : vérifier sa validation par l'enseignant et écrire ses résultats attendus dans `RECETTE.md`. Une règle, une vérification, puis consignation de l'observé. Objectif final : 20 à 30 cas, au moins deux par règle et un par interaction déclarée, avec les cas limites.
- Documenter les décisions et les résultats réellement obtenus au fil du travail. `QUESTIONS.md` reçoit les réponses aux questions du professeur ; `ECHECS.md` décrit trois échecs réels de l'IA (demande, résultat, détection, correction de la demande). Ne rien fabriquer ni antidater.
- Conserver les journaux bruts individuels dans `sessions/<prénom>/`, sans retouche. Ne pas supposer qu'un agent les y exporte automatiquement. Pour chaque tâche autorisée, laisser une trace concise des changements, tests et points ouverts afin de permettre la reprise.
- Les règles étaient déjà codées dans l'archive : ne pas présenter une recette rédigée ensuite comme antérieure au code. Conserver les preuves existantes et documenter honnêtement la suite.
- La prochaine tâche reste soumise à validation de l'utilisateur. Lire `SUIVI.md` pour reprendre ; ne pas corriger les problèmes connus ou poursuivre la séance automatiquement.
