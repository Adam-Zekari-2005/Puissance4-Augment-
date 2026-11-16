# Questionnaire de cas limites

Groupe : Rayhan DAHMANI, Adnane BOUCHEHIT, Adam ZEKARI, Valentin PREVOT — 16/11/2026

Le PDF de séance 4 annonce huit questions remises par l'enseignant ; en séance, l'enseignant a indiqué au groupe qu'il ne fournit pas les questions et que c'est au groupe de les écrire. Les huit questions ci-dessous couvrent les six situations listées par le PDF. Les décisions ont été proposées par Claude Code puis validées par le groupe le 16/11/2026, avant d'observer le comportement du code pour les questions non encore démontrées.

Chaque réponse contient la **décision** et la **démonstration** : `rejouer(coups, REGLES)` avec les cinq règles actives, l'état obtenu et sa correspondance avec la décision. Les démonstrations renvoient aux cas de `RECETTE.md`. Notation : colonnes 0 à 6, ligne 0 en haut, retrait en colonne `c` noté `-(c+1)`.

## Q1 — Un coup forme un carré et cinq alignés pour le même joueur

*Type : deux règles se déclenchent au même tour.*

**Décision :** le joueur **perd**, l'adversaire gagne. La Règle 4 (trop aligné) est vérifiée en premier et la priorité 2 de `APRES_COUP` (« A perd → B gagne ») passe avant la priorité 5 (« A gagne »). Décision déjà présente dans le règlement v1 (cas limite de la Règle 3, interaction « 3 et 4 »).

**Démonstration :** cas 28 de `RECETTE.md`. `rejouer([2,0,3,1,0,4,1,5,3,6,4,5,2], REGLES)` : ligne 4 `X X X X X O .` (cinq X) et carré X `[4][2]`, `[4][3]`, `[5][2]`, `[5][3]` ; gagnant `O`, `fini=True`. Conforme à la décision.

## Q2 — Le 84e coup fait gagner un joueur

*Type : deux règles se déclenchent au même tour (victoire et limite de durée).*

**Décision :** la **victoire** l'emporte sur le match nul de la limite de 84 coups. La victoire est vérifiée à `APRES_COUP`, qui arrête la partie avant `FIN_DE_TOUR`, où se trouve la limite. Le règlement v1 ne le disait pas explicitement : décision à écrire dans le règlement v2.

**Démonstration :** cas 33 de `RECETTE.md`, suite `V84` (84 coups, recopiée dans la recette). `rejouer(V84[:83], REGLES)` : partie en cours, à O de jouer. Au 84e coup, O joue la colonne 4 et forme le carré `[3][3]`, `[3][4]`, `[4][3]`, `[4][4]` : `rejouer(V84, REGLES)` donne gagnant `O` (et non `nul`), `fini=True`, 84 coups. Conforme à la décision : le code respectait déjà cet ordre, la décision le rend explicite.

## Q3 — Un jeton gris est dû mais les colonnes 1, 3 et 5 sont pleines

*Type : une règle ne peut plus s'appliquer (plus de colonne valide).*

**Décision :** **aucun gris** n'est posé, la partie continue. Le gris suivant garde sa colonne prévue : le k-ième gris vise toujours `[1, 3, 5][(k-1) % 3]`. Décision déjà présente dans le règlement v1 (cas limite de la Règle 2).

**Démonstration :** cas 34 de `RECETTE.md`, suite `P60` (60 coups, recopiée dans la recette). Avec `rejouer(P60[:k], REGLES)` : au coup 15, la colonne 1 est pleine et le 1er gris va en colonne 3 ; aux coups 30 et 45, les colonnes 1, 3 et 5 sont pleines et aucun gris n'est posé (un seul gris sur la grille), la partie continue ; au coup 60, le 4e gris garde sa colonne prévue `[1,3,5][(4-1) % 3]` et tombe en colonne 1, en `[1][1]`, bien que la colonne 5 soit libre. Conforme à la décision.

## Q4 — Un Pop out donne quatre alignés à l'adversaire

*Type : une règle crée un alignement pour l'adversaire de celui qui vient de jouer.*

**Décision :** l'**adversaire gagne**. Les deux joueurs sont évalués après chaque coup ; seul l'adversaire « gagne », donc priorité 6. Décision déjà présente dans le règlement v1 (interaction « 1 et 3/4/5 »).

**Démonstration :** cas 20 de `RECETTE.md`. `rejouer([0,0,1,1,3,2,3,2,6,3,-4], REGLES)` : le retrait de X en colonne 3 fait descendre la pile ; quatre O en ligne 4, colonnes 0–3 ; gagnant `O`, `fini=True`. Conforme à la décision.

## Q5 — Un Pop out donne cinq alignés aux deux joueurs

*Type : les deux joueurs se retrouvent alignés en même temps.*

**Décision :** **match nul**. Les deux joueurs « perdent » : priorité 1 de `APRES_COUP`. Décision déjà présente dans le règlement v1 (cas limite de la Règle 4, interaction « 1 et 4 »).

**Démonstration :** cas 30 de `RECETTE.md`. `rejouer([0,1,2,0,3,2,1,3,4,1,6,4,6,-2], REGLES)` : après le retrait de O en colonne 1, ligne 4 `O O O O O . X` et ligne 5 `X X X X X . X` ; résultat `nul`, `fini=True`. Conforme à la décision.

## Q6 — Grille pleine, le joueur suivant n'a aucun jeton sur la ligne du bas

*Type : une règle s'applique alors que la grille est pleine.*

**Décision :** **match nul** : le joueur ne peut ni poser ni retirer. Décision déjà présente dans le règlement v1 (`FIN_DE_TOUR`). La situation peut réellement arriver : la ligne du bas peut ne contenir que des jetons d'un joueur séparés par un gris.

**Démonstration :** cas 35 de `RECETTE.md`, suite `N53` (53 coups, recopiée dans la recette). `rejouer(N53[:52], REGLES)` : partie en cours, à X de jouer, seule la case `[0][3]` est vide, ligne du bas `X X X G X X X` (le gris coupe les X en deux groupes de trois). Au 53e coup, X remplit `[0][3]` : grille pleine, aucun alignement de quatre, carré ni sandwich ; O n'a aucun jeton en bas. `rejouer(N53, REGLES)` donne `nul`, `fini=True`, aucun coup possible, joueur `O` (le nul est vérifié à `FIN_DE_TOUR`, après le passage de main). Conforme à la décision.

## Q7 — Un Pop out retire le jeton situé sous un gris

*Type : une règle défait l'effet d'une autre.*

**Décision :** le **gris descend** d'une case avec la pile. S'il arrive sur la ligne du bas, il ne peut pas être retiré et bloque le Pop out de cette colonne pour les deux joueurs. Décision déjà présente dans le règlement v1 (interactions « 1 et 2 »).

**Démonstration :** cas 32 de `RECETTE.md`. `rejouer([1,6,6,6,6,6,6,3,3,3,3,3,3,0,5,0,-2], REGLES)` : après le 15e coup, le gris tombe en `[4][1]` sur le X de `[5][1]` ; au 17e coup, X retire ce X et le gris descend en `[5][1]` (ligne 5 `O G . O . X O`), partie en cours. Les coups possibles de O sont `[0,1,2,4,5,-1,-4,-7]`, sans `-2`, et `jouer(etat, -2)` lève `ValueError` sans modifier l'état. Conforme à la décision.

## Q8 — Le 15e coup fait gagner un joueur

*Type : une règle défait l'effet d'une autre (la victoire annule la chute du gris).*

**Décision :** **aucun gris** n'est posé : la partie est finie à `APRES_COUP`, avant `FIN_DE_TOUR`. Décision déjà présente dans le règlement v1 (interaction « 2 et fin de partie »).

**Démonstration :** cas 31 de `RECETTE.md`. `rejouer([0,6,6,6,6,6,6,3,3,3,1,3,0,3,1], REGLES)` : au 15e coup, X forme le carré `[4][0]`, `[4][1]`, `[5][0]`, `[5][1]` ; gagnant `X`, `fini=True`, et la grille ne contient aucun gris (le gris aurait visé la colonne 1). Après 14 coups, la partie était en cours, sans gris. Conforme à la décision.
