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

Avant toute fusion dans `main`, accord du groupe et vérification des points bloquants. Le périmètre du problème de règles globales est précisé ci-dessous.

## 2026-11-13 — Diagnostic de l'isolation des parties

Correction autorisée par l'utilisateur ; diagnostic réalisé, puis périmètre recentré à sa demande sur les exigences des PDF. Moteur inchangé.

- Essai local de `test_isolation.py` : conservation d'une victoire par carré après un rejeu standard, et conservation des coups autorisés lorsque des parties de modes différents se succèdent.
- `python -B -m unittest test_isolation -v` : **2 tests, 2 échecs**, reproduisant le défaut attendu. Le moteur, les règles et les tests existants n'ont pas été modifiés.
- Après `[0,0]`, les deux modes produisent les mêmes valeurs dans les sept champs actuels, mais seul le mode augmenté autorise le retrait `-1`. Les valeurs de l'état ne suffisent donc pas à déterminer son mode.
- Relecture du PDF de séance 2, annexe A : les noms, paramètres et la forme de l'état ne changent pas. Aucun ajout de métadonnée à l'état n'est réalisé.
- Les PDF n'exigent pas explicitement la coexistence de parties utilisant des modes différents. Les deux tests ajoutaient cette exigence ; le fichier expérimental a donc été retiré après la demande de suivre uniquement les consignes du professeur. Leurs résultats ci-dessus restent conservés comme diagnostic, pas comme tests du contrat imposé.
- Limite actuelle, non corrigée : un seul ensemble de règles actif dans le moteur. Pour consulter ou poursuivre une ancienne partie après un changement de mode, réactiver son ensemble de règles avec `activer_regles(...)`. Ce fonctionnement décrit le code existant ; ce n'est pas une consigne du professeur.
- Ne pas annoncer une isolation des parties ni une conformité complète. Le socle 16/16 et les règles 21/21 ont été vérifiés lors de l'intégration. La suite du travail doit porter sur la recette et la conformité au règlement, après validation de l'utilisateur.

## 2026-11-13 — Mise en commun sur main

- L'utilisateur autorise explicitement l'intégration et la publication de la base commune dans `main`.
- Après récupération distante, `main` et les quatre branches personnelles (`adnane`, `adam`, `Rayhan`, `valentin`) pointent sur `b16585f` ; aucune divergence distante avec la base de l'intégration. Les changements locaux non publiés des autres membres ne sont pas visibles ici.
- Publication prévue par avance rapide, sans réécriture d'historique ni modification des branches personnelles. Le README indique comment chacun intègre `origin/main` sur sa branche ; son encodage a été converti d'UTF-16 en UTF-8.
- Derniers ajustements : documentation uniquement. Le moteur, les règles et les deux suites restent identiques aux fichiers vérifiés à 16/16 et 21/21 lors de l'intégration.

## 2026-11-13 — Première version du cahier de recette

- Tâche autorisée sur `adnane` : créer `RECETTE.md` avec résultats attendus, sans lancer la campagne ni remplir les observations.
- 26 cas issus du règlement et des tests existants, avec quelques préfixes pour vérifier les non-déclenchements. Les suites longues sont recopiées explicitement ; les attentes ne sont pas déduites d'une nouvelle exécution du moteur.
- Chronologie indiquée : le code et les tests de l'archive précèdent ce cahier. Observé et verdict laissés vides. Les interactions et cas limites non couverts sont listés, sans annoncer une couverture complète.
- Contexte actualisé dans `AGENTS.md`. Aucun changement de code, des tests ou du règlement ; aucun lancement de la nouvelle campagne. Les 16 tests du socle ont été revérifiés avec succès juste avant cette tâche, à la demande de l'utilisateur.
- Prochaine étape, après accord : relire les attentes avec le groupe puis vérifier les cas et renseigner les observations réelles.

## 2026-11-13 — Exécution des 26 cas de recette

- Campagne autorisée par l'utilisateur sur `adnane`, réalisée par Codex avec Python Windows et `-B`, au moyen d'un script exécuté en mémoire. Aucun changement du moteur, des règles ou des tests existants.
- Exécution des 26 procédures de `RECETTE.md`, avec comparaison aux attentes préalablement écrites : **26 conformes, 0 échec**. Les vérifications incluent les coordonnées des jetons, les motifs, les refus avec état inchangé, les coups disponibles, les compteurs, le passage du 83e au 84e coup, l'immutabilité et l'égalité des états rejoués.
- Le cas 21 a également contrôlé les motifs des deux joueurs : chacun possède un alignement maximal de quatre, aucun de cinq ; résultat nul. Cas 22 : seuls les retraits `[-3,-5,-6]` sont possibles sur la grille pleine.
- Observations datées et verdicts renseignés dans le cahier sans modifier les attentes. Aucun échec inventé. Les résultats sont ceux des appels Python, pas d'une partie jouée dans une interface.
- La couverture reste incomplète : les interactions manquantes et l'écart de changement de joueur terminal restent signalés. La réussite de cette campagne ne les valide pas.
- `AGENTS.md` actualisé ; responsable du cahier : Adnane BOUCHEHIT. Modifications documentaires locales, non publiées à ce stade.
