# Puissance 4 augmenté

`main` contient la base commune du groupe. Chacun développe sur sa branche : `adnane`, `adam`, `Rayhan` ou `valentin`.

## Récupérer la base commune

Vérifiez d'abord `git status`. Si vous avez du travail non enregistré, sauvegardez-le dans un commit sur votre branche avant de continuer. Remplacez `ma-branche` par son nom exact :

```sh
git fetch origin
git switch ma-branche
git merge origin/main
git push
```

Si votre branche n'existe pas localement, remplacez le deuxième appel par `git switch --track origin/ma-branche`. En cas de conflit, résolvez-le avec le groupe ; ne forcez pas le push.

## Fichiers et vérifications

- `REGLEMENT-v1.md` : règlement de référence, contenu à préserver.
- `moteur.py`, `regles.py` : moteur et cinq règles repris de la base du groupe.
- `AGENTS.md` : contexte commun des agents ; `CLAUDE.md` y renvoie.
- `SUIVI.md` : décisions, vérifications et limites connues.
- PDF du professeur : conservés localement, exclus du dépôt comme les caches Python.

```sh
python -B test_socle.py moteur
python -B test_reglement.py
```

Jouer : `python jeu.py` (cinq règles actives).

Dernière vérification : **16/16** tests du socle et **21/21** tests des règles. Lire les limites dans `SUIVI.md`. Les changements personnels sont à relire et tester avant leur intégration dans `main`.
