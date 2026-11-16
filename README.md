# Puissance 4 augmenté

Groupe : Rayhan DAHMANI, Adnane BOUCHEHIT, Adam ZEKARI, Valentin PREVOT.

Puissance 4 en Python, interface terminal, avec cinq règles maison : Pop out, jeton gris, carré, trop aligné et sandwich horizontal.

## Où trouver les livrables

| Fichier | Contenu |
|---|---|
| `REGLEMENT-v1.md` | Règlement remis en séance 2, conservé intact. |
| `REGLEMENT-v2.md` | Règlement après la séance 4 : ajouts marqués **(v2)**, tableau « Changements depuis la v1 » en fin de fichier. |
| `QUESTIONS.md` | Les huit questions de cas limites, chacune avec sa décision et sa démonstration. |
| `RECETTE.md` | Cahier de recette : 36 cas avec attendu, observé et date ; couverture restante en fin de fichier. |
| `moteur.py`, `regles.py`, `jeu.py` | Moteur (signatures imposées), cinq règles branchées sur le point d'accroche, interface terminal. |
| `AGENTS.md` (`CLAUDE.md` y renvoie) | Contexte du projet et contrat d'interface, lus par les agents. |
| `SUIVI.md` | Journal des décisions, vérifications, erreurs et limites connues. |

À venir : `REGLEMENT-v3.md`, `ECHECS.md` et `sessions/<prénom>/` (journaux bruts de chaque membre).

## Jouer et vérifier

```sh
python jeu.py                     # partie à deux au clavier, cinq règles actives
python -B test_socle.py moteur    # 16 tests du socle standard
python -B test_reglement.py       # 21 tests des règles
python -B -m unittest test_fin_partie -v   # 3 tests de fin de partie
```

Pose : colonne `0` à `6`. Pop out : `-1` pour la colonne 0, jusqu'à `-7` pour la colonne 6.

## Travail en groupe

`main` contient la version commune. Chacun développe sur sa branche (`adnane`, `adam`, `Rayhan`, `valentin`). Pour récupérer `main`, vérifiez d'abord `git status` et enregistrez votre travail dans un commit, puis :

```sh
git fetch origin
git switch ma-branche
git merge origin/main
git push
```

Si votre branche n'existe pas localement : `git switch --track origin/ma-branche`. En cas de conflit, résolvez-le avec le groupe ; ne forcez pas le push. Les PDF du professeur et les caches Python sont exclus du dépôt.
