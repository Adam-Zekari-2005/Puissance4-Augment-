# Puissance 4 augmenté

Groupe : Rayhan DAHMANI, Adnane BOUCHEHIT, Adam ZEKARI, Valentin PREVOT.

Puissance 4 en Python, interface terminal, avec cinq règles maison : Pop out, jeton gris, carré, trop aligné et sandwich horizontal.

## Où trouver les livrables

| Fichier | Contenu |
|---|---|
| `REGLEMENT-v1.md` | Règlement remis en séance 2, conservé intact. |
| `REGLEMENT-v2.md` | Règlement après la séance 4 : ajouts marqués **(v2)**, tableau « Changements depuis la v1 » en fin de fichier. |
| `QUESTIONS.md` | Les huit questions de cas limites, chacune avec sa décision et sa démonstration. |
| `RECETTE.md` | Cahier de recette : 43 cas avec attendu, observé et date ; campagne complète du 20/11/2026 et tableau de couverture. |
| `ECHECS.md` | Trois incidents documentés, demandes reconstituées et précisions rétrospectives. |
| `moteur.py`, `regles.py`, `jeu.py` | Moteur (signatures imposées), cinq règles branchées sur le point d'accroche, interface terminal. |
| `AGENTS.md` (`CLAUDE.md` y renvoie) | Contexte du projet et contrat d'interface, lus par les agents. |
| `SUIVI.md` | Journal des décisions, vérifications, erreurs et limites connues. |

À venir : `REGLEMENT-v3.md` et `sessions/<prénom>/` (journaux bruts de chaque membre).
La recette doit être relue par le groupe.

## Jouer et vérifier

```sh
python jeu.py                     # menu : deux joueurs, ordinateur ou rejeu
python -B test_socle.py moteur    # 16 tests du socle standard
python -B test_reglement.py       # 21 tests des règles
python -B -m unittest test_fin_partie -v   # 3 tests de fin de partie
python -B -m unittest test_lot4 -v  # outils terminal et 30 parties simulées
```

Pose : colonne `0` à `6`. Pop out : `-1` pour la colonne 0, jusqu'à `-7` pour la colonne 6.

Le menu propose `1` pour deux joueurs, `2` contre l'ordinateur (vous : X,
ordinateur : O), `3` pour rejouer une liste de coups, et `q` pour quitter.
Les cinq règles sont actives dans tous ces modes. L'ordinateur choisit au hasard
parmi les coups autorisés, retraits compris.

Pendant une partie, saisir `h` affiche l'historique sans jouer de coup.
La liste est aussi affichée à la fin ou lors d'une interruption. Copiez-la,
puis collez-la dans le mode `3`, par exemple `[0, 0, -1]` : la grille,
le résultat et l'historique reconstruits sont affichés. Une liste incorrecte
ou contenant un coup illégal est refusée ; `q` revient au menu principal.

## Travail en groupe

`main` contient la version commune. Chacun développe sur sa branche (`adnane`, `adam`, `Rayhan`, `valentin`). Pour récupérer `main`, vérifiez d'abord `git status` et enregistrez votre travail dans un commit, puis :

```sh
git fetch origin
git switch ma-branche
git merge origin/main
git push
```

Si votre branche n'existe pas localement : `git switch --track origin/ma-branche`. En cas de conflit, résolvez-le avec le groupe ; ne forcez pas le push. Les PDF du professeur et les caches Python sont exclus du dépôt.
