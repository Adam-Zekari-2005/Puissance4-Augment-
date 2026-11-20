# Puissance 4 augmenté

## Contexte et sources
- Projet universitaire : Puissance 4 en Python, interface terminal, cinq règles originales. Le professeur évalue surtout la précision des spécifications et leur vérification.
- Base de fin de séance 2 récupérée sur le PC d'un membre du groupe : elle contient déjà les cinq règles codées. Codex est l'agent principal, Claude Code prend le relais si nécessaire. Son utilisation est autorisée par le professeur selon l'utilisateur.
- Consignes de référence : les PDF « Puissance 4 augmenté — Séance 1.pdf » à « Séance 4.pdf » (hors dépôt). En séance 4, l'enseignant a indiqué que le groupe écrit lui-même les huit questions, contrairement aux PDF, et qu'il est possible de dépasser 30 cas de recette sans abuser.
- Règlement : `REGLEMENT-v1.md` (remis, à ne jamais modifier) et `REGLEMENT-v2.md` (version courante, ajouts marqués **(v2)**). Lire la v2 avant toute tâche liée aux règles ; ne pas la recopier ici ni inventer les informations manquantes.

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
- Écart du joueur terminal corrigé le 16/11/2026 : passage de main seulement à `FIN_DE_TOUR`, après les victoires/défaites. Le dernier joueur est déduit de la parité de `len(coups)` (X commence). Cas 27 de recette vérifié ; tests complémentaires : `python -B -m unittest test_fin_partie -v`.

## État vérifié et reprise
- Mise à jour séance 5 (20/11/2026) : outils du lot 4 réalisés dans `jeu.py` (ordinateur aléatoire, historique, rejeu). `test_lot4.py` : quatre tests réussis, dont 30 parties simulées rejouées à l'identique. `RECETTE.md` contient désormais 43 cas : campagne complète 43/43, observations datées et historique du cas 27 conservé, tableau de couverture des interactions. Observations produites par exécution Python, à relire par le groupe. `ECHECS.md` contient trois incidents documentés, des demandes reconstituées et des précisions rétrospectives. Voir la première entrée de `SUIVI.md` pour les preuves et limites actuelles. Les mentions 36 cas et absence d'ECHECS ci-dessous décrivent la fin de séance 4.
- `moteur.py`, `regles.py` et `test_reglement.py` proviennent de l'archive `Travailler IA.zip`. Le règlement a seulement été renommé ; `test_socle.py` est inchangé.
- Les tests de l'archive ont réussi : 16/16 pour le socle, 21/21 pour les règles. Commande complémentaire : `python -B test_reglement.py`. Ces résultats ne prouvent pas la conformité complète ; les limites et vérifications d'intégration sont dans `SUIVI.md`.
- `RECETTE.md` contient 36 cas, tous conformes au 16/11/2026 (cas 01–26 du 13/11, cas 27 en échec puis corrigé, cas 28–36 ajoutés en séance 4). Sa section « Couverture à compléter » liste les interactions encore sans cas dédié. Adnane BOUCHEHIT est responsable du cahier selon sa demande. `jeu.py` permet une partie à deux au clavier avec pose, retrait, refus, messages de déclenchement et résultat final (vérifié par deux parties simulées complètes). Les messages proviennent de `regles.decrire_evenements(avant, coup, apres)`, pour un coup accepté avec les cinq règles actives.
- `QUESTIONS.md` contient les huit questions du groupe, leurs décisions (validées par le groupe) et leurs démonstrations (cas 20, 28, 30 à 35). Les longues suites de démonstration (`V84`, `P60`, `N53`, cas 36) ont été trouvées par un script de recherche hors dépôt, indépendant du moteur ; les attendus viennent du règlement ou des décisions, jamais du moteur. `ECHECS.md` et `sessions/` restent absents. La validation professorale des règles et l'attribution des autres lots ne sont pas attestées dans les fichiers.
- Pour une nouvelle collision (méthode séance 4) : reproduire, trancher en groupe, écrire la décision dans le règlement (nouvelle version), écrire l'attendu dans `RECETTE.md` avant d'exécuter, puis corriger le code si besoin. Une vérification à la fois, observé consigné. Objectif : au moins deux cas par règle et un par interaction déclarée, avec les cas limites.
- Documenter les décisions et les résultats réellement obtenus au fil du travail. `QUESTIONS.md` reçoit les réponses aux huit questions ; `ECHECS.md` décrit trois échecs réels de l'IA (demande, résultat, détection, correction de la demande). Ne rien fabriquer ni antidater.
- Conserver les journaux bruts individuels dans `sessions/<prénom>/`, sans retouche. Ne pas supposer qu'un agent les y exporte automatiquement. Pour chaque tâche autorisée, laisser une trace concise des changements, tests et points ouverts afin de permettre la reprise.
- Les règles étaient déjà codées dans l'archive : ne pas présenter une recette rédigée ensuite comme antérieure au code. Conserver les preuves existantes et documenter honnêtement la suite.
- La prochaine tâche reste soumise à validation de l'utilisateur. Lire `SUIVI.md` pour reprendre ; ne pas corriger les problèmes connus ou poursuivre la séance automatiquement.
