# Suivi du projet

## 2026-11-13 — Intégration de la base du groupe

Tâche autorisée : reprendre la base fournie dans `Travailler IA.zip` sur une branche dédiée, sans corriger le code ni développer de nouvelles fonctionnalités.

- Branche : `integration-seance2`, créée depuis `origin/main`. Fusion dans `main` soumise à l'accord du groupe.
- Importés sans changement : `moteur.py`, `regles.py`, `test_reglement.py`.
- `REGLEMENT-v1 (1).md` renommé en `REGLEMENT-v1.md` sans modification de contenu. Son texte est identique à celui de l'archive ; `test_socle.py` est également identique et conservé.
- `AGENTS.md` actualisé avec le contrat technique de l'archive et les limites connues. `CLAUDE.md` conserve le renvoi vers cette source commune. README et exclusions Git conservés.
- Non importés : doublon `Claude outputs/REGLEMENT-v1.md`, caches Python et `Modelfile` contenant un modèle non renseigné. PDF exclus du dépôt.

## Vérifications

- Comparaison préalable : règlement et tests standard identiques après normalisation des fins de ligne.
- Tests de l'archive exécutés en mémoire : socle **16/16**, règlement **21/21**.
- Vérification des fichiers intégrés : `python -B test_socle.py moteur` **16/16** et `python -B test_reglement.py` **21/21**, sorties sans échec. Aucun test ajouté ou modifié.

## Points ouverts — aucune correction dans cette intégration

1. **Règles globales : défaut reproduit.** Après `e = moteur.rejouer([0,6,1,6,0,5,1], REGLES)`, `gagnant(e)` vaut `X`. Après `moteur.rejouer([])`, `gagnant(e)` vaut `None` alors que `e['fini']` reste vrai. Le mode global change donc l'interprétation d'un état existant. Les suites actuelles ne couvrent pas ce cas.
2. **Changement de joueur : écart à clarifier.** Le code change le joueur avant de vérifier la victoire, même sur un coup terminal. Le tableau du contexte d'origine et le règlement situent ce changement après cette vérification. Ne pas trancher sans validation.
3. **Livrables manquants :** interface `jeu.py`, recette, questions, échecs et journaux individuels. Les 21 tests automatisés ne remplacent pas `RECETTE.md` ; ne pas antidater les attentes ni inventer l'historique de développement.

Prochaine tâche proposée : traiter le défaut des règles globales avec un cas de vérification ciblé, après validation. Avant toute fusion dans `main`, accord du groupe et vérification des points bloquants.
