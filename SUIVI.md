# Suivi du projet

## 2026-11-16 — Recette, cas 28 (R3 + R4)

- Réalisé par Claude Code sur `adnane`, à la demande de l'utilisateur. Avant : `git fetch origin`, branche à jour avec `origin/adnane` (`9f8556d`) ; socle 16/16, règles 21/21, `test_fin_partie` 3/3.
- Incident préalable : `RECETTE.md` avait été modifié localement par erreur (section du cas 27 supprimée). Restauré avec `git restore RECETTE.md` après accord de l'utilisateur.
- Cas 28 ajouté dans `RECETTE.md` (section « Cas d'interaction ajoutés ») : un coup forme à la fois un carré et cinq alignés pour X. Attendu écrit depuis le règlement v1 (Règle 3 cas limite, interaction « 3 et 4 », priorité 2), suite construite à la main, avant exécution.
- Exécution en mémoire avec Python et `-B` : **conforme** (O gagne, fini=True, joueur X conservé, 13 coups ; préfixe sans gagnant ni gris ; immutabilité et rejeu identiques). Moteur, règles, tests et règlement inchangés. Aucun commit ni push.
- Cas 29 ajouté (R3 + R5 : carré et sandwich au même coup, priorité 5), attendu écrit avant exécution puis vérifié : **conforme** (X gagne, fini=True, joueur X, 13 coups ; préfixe sans gagnant ni gris ; immutabilité et rejeu identiques).
- Cas R4/R5 reporté : sandwich et cinq alignés créés par un même jeton imposent un alignement de cinq en diagonale (impossible en horizontal sur 7 colonnes avec le sandwich, impossible en vertical sans quatre alignés préalables) ; suite plus longue à construire.
- Couverture encore ouverte : priorité R4/R5, deux défaites simultanées après Pop out, interactions des gris et cas limites listés dans `RECETTE.md`.
- Vérification de `jeu.py` (point d'étape séance 3 : partie entière au clavier), par deux lancements avec entrées simulées, sans modification de fichier. Partie 1 : `abc`, `9`, `-1` redemandés (saisie incorrecte, coup interdit), puis suite du cas 28 : messages « Trop aligné », « Carré », priorité de la défaite, « Le joueur O gagne ! ». Partie 2 : suite `L84` complète (84 coups, Pop out et gris annoncés, gris affichés `G`), aucun refus, « Limite de 84 coups atteinte : match nul » puis « Match nul. ». Code retour 0, aucun plantage.
- Branche `Knoce` (Rayhan) observée après `git fetch` : essais personnels selon l'utilisateur, non intégrés ; Rayhan reprendra la version de `main`.

## 2026-11-16 — Correction du joueur terminal

- Correction autorisée : `jouer` passe la main à `FIN_DE_TOUR` uniquement après la vérification des victoires/défaites. `_resultat_victoire` identifie le dernier joueur par la parité de l'historique, valable avant et après le passage de main puisque X commence et chaque action acceptée compte un coup.
- Signatures, forme de l'état, compteur de tours et règlement v1 inchangés. Les nuls de fin de tour restent évalués après le passage de main ; un nul par victoires simultanées arrête avant celui-ci.
- Ajout de `test_fin_partie.py` : trois tests, dont six scénarios terminaux (X, O, défaite, sandwich adverse, retrait et mode standard), avec immutabilité, rejeu et refus après fin ; continuation et nul de fin de tour. Tous passent avec Python Windows et `-B`.
- Contrôles en mémoire des suites `DOUBLE`, `L84`, `S15` et `PLEINE` lus dans la recette : résultats, joueurs, immutabilité et rejeu conformes. Socle **16/16**, règles **21/21** ; fichiers de ces tests inchangés. Cas 27 désormais conforme, échec initial conservé. Les 26 cas historiques n'ont pas tous été réexécutés.
- Erreur réelle dans le nouveau test : la première suite prévue pour une victoire de O faisait déjà gagner X par carré au coup précédent. Le refus du moteur était correct ; remplacement des coups de X pour éviter ce carré, puis test réussi. Aucun changement de moteur pour contourner cet échec.
- Documentation actualisée dans `AGENTS.md` et `RECETTE.md`. Les autres limites de couverture et de règles globales restent ouvertes. Aucun commit ni push.

## 2026-11-16 — Diagnostic du joueur terminal

- Étape autorisée : vérifier l'écart et préparer sa correction avec un cas de recette. Moteur et règlement inchangés.
- Cas 27 ajouté dans `RECETTE.md` : après `[0,6,1,6,0,5,1]`, résultat X et fini=True, mais joueur O ; le règlement arrête pourtant le traitement avant le passage de main. Le préfixe de six coups donne bien joueur X, sans gagnant.
- Contrôle complémentaire : `[6,0,6,1,5,3,6,4,2]` fait gagner O par sandwich après une pose de X ; le joueur terminal doit donc rester le poseur X, pas nécessairement le gagnant.
- Correction proposée : déplacer le changement de joueur dans `FIN_DE_TOUR`, après la vérification des victoires/défaites. Vérifier aussi l'identification du dernier joueur dans `_resultat_victoire`, qui suppose actuellement que la main a déjà changé. Préserver les signatures et la forme de l'état ; ne pas modifier le règlement.
- Après autorisation de la correction : contrôler victoire, défaite, victoire adverse, nul simultané, continuation et nul de fin de tour ; vérifier immutabilité et rejeu, puis relancer les 16 tests du socle et les 21 tests des règles.
- Diagnostic exécuté avec Python Windows et `-B`. Premier lancement inaccessible dans le bac à sable, puis exécution autorisée réussie. Aucun test des suites existantes relancé à cette étape ; aucun commit ni push.

## 2026-11-16 — Lot 3, messages des règles

- Ajout autorisé de `decrire_evenements(avant, coup, apres)` dans `regles.py`, appelée par `jeu.py` après chaque coup accepté avec les cinq règles actives. Réutilisation des fonctions de détection des règles et de l'alignement du moteur.
- Messages pour Pop out, apparition d'un gris, carré, cinq alignés, sandwich et causes de match nul. Les motifs sont décrits puis les priorités sont précisées, le résultat final étant fourni par `gagnant`.
- Contrôles ciblés réussis sur suites connues pour chaque règle, double victoire et limite de 84 coups. Contrôles sur états construits réussis pour gris déplacé par retrait, carré avec cinq alignés et deux défaites simultanées. Les états reçus restent identiques après description.
- Trois lancements complets de `jeu.py` avec entrées simulées vérifient les messages et résultats pour carré, sandwich adverse et match nul au coup 84. Socle 16/16 et règlement 21/21 réussis.
- Cette fonction décrit les cinq règles du projet et suppose un coup accepté reliant les deux états. Les contrôles de motifs simultanés sur états construits complètent les essais de parties et sont distingués ici pour leur traçabilité.
- Modifications locales sur `adnane`, en attente de publication demandée par l'utilisateur. La couverture de recette et l'écart concernant le joueur terminal restent documentés.

## 2026-11-16 — Lot 3, saisie et partie complète

- Étape autorisée sur `adnane` après récupération de l'affichage d'Adam. `jeu.py` active les cinq règles, accepte les entiers de pose et retrait, consulte `coups_possibles`, applique `jouer`, réaffiche la grille et annonce le résultat de `gagnant`.
- Saisie incorrecte ou coup interdit entraînent une nouvelle demande. Fin d'entrée ou Ctrl+C interrompent proprement la saisie.
- Contrôles par lancement réel de `jeu.py` avec entrées simulées réussis pour saisies invalides puis carré gagnant, Pop out puis fin d'entrée, cinq alignés faisant gagner O, et partie complète de 84 coups avec gris et retraits aboutissant au match nul. Les 16 tests du socle et 21 tests des règles passent.
- Une assertion du script de contrôle sur « Partie terminée. » a échoué à cause de l'encodage PowerShell du caractère accentué. Vérification corrigée avec une séquence Unicode, puis réussie. Aucun défaut du jeu associé à cet échec de contrôle.
- Les messages détaillés indiquant quelle règle se déclenche restent une étape distincte, comme prévu dans le suivi d'Adam. Règlement, moteur et règles conservés. Aucun push pour cette étape à ce stade.

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

## 2026-11-13 — Lot 3 : premier affichage terminal

- Travail sur `adam`, au commit `e9c8cd9`, identique à la référence `origin/main` récupérée ; dossier initialement propre. Aucune fusion ni publication.
- PDF de séance 3 fourni par l'utilisateur et lu visuellement (5 pages). Il demande une interface terminal utilisant le contrat, les messages de déclenchement et une partie entière au clavier. Le PDF de séance 2 reste non retrouvé.
- Première étape réalisée : `jeu.py`, fonction `afficher_grille(etat)`, colonnes numérotées, ligne 0 en haut, symboles X/O/G et point pour une case vide, légende, joueur et tour. Un état fini est signalé sans annoncer un prochain joueur. `python -B jeu.py` affiche seulement la grille initiale : la boucle de saisie reste à réaliser.
- Vérifications : socle 16/16, règlement 21/21 ; contrôle en mémoire de quatre états (vide, empilement X/O, jeton gris après 15 coups, victoire par carré), orientation et absence de mutation. Une assertion du script de contrôle avait une ligne du bas attendue erronée ; corrigée après relecture de la suite, puis contrôle réussi, sans changement du moteur.
- Moteur, règles, règlement et recette inchangés. Les 26 cas de recette n'ont pas été réexécutés.
- Point ouvert : le contrat ne fournit pas de journal des déclenchements. Proposition à discuter avec le groupe : une fonction de diagnostic côté moteur/règles qui expose les événements, sans changer les signatures ni les champs imposés. Aucun ajout de contrat ni duplication des règles dans l'interface à cette étape.
