# Puissance 4 augmenté — règlement v2
Groupe : Rayhan DAHMANI, Adnane BOUCHEHITE, Adam ZEKARI, Valentin PREVOT    Date : 16/11/2026

Cette version reprend `REGLEMENT-v1.md` (conservé intact) et y intègre ce qui a été tranché en séance 4 : les réponses aux huit questions de `QUESTIONS.md` et les écarts découverts pendant la recette. Chaque ajout est marqué **(v2)** et renvoie à sa question (Q1 à Q8) ou à son cas de `RECETTE.md`. La liste complète est en fin de document.

## Jeu de base
Puissance 4 standard, grille 7 × 6. Les règles ci-dessous s'y ajoutent.

**Conventions (celles du contrat `moteur.py`) :**
- Joueurs `X` (commence) et `O`. Jeton gris : `G`, il n'appartient à personne.
- Colonnes **0 à 6** de gauche à droite ; **ligne 0 = haut, ligne 5 = bas** ; une case se note `grille[ligne][colonne]`.
- Un **coup** est l'action d'un seul joueur (poser ou retirer). Le **numéro du coup** vaut `len(coups)` une fois le coup joué.
- Dans `coups`, poser en colonne `c` s'écrit `c` ; retirer (Pop out, Règle 1) en colonne `c` s'écrit `-(c+1)` : `-1` = colonne 0, …, `-7` = colonne 6.
- Un coup **refusé** (illégal) : `jouer()` lève `ValueError` et l'état reçu n'est pas modifié ; c'est toujours au même joueur. Une fois la partie finie, tout coup est refusé.
- **Alignement** : jetons consécutifs d'un même joueur, horizontalement, verticalement ou en diagonale (↗ ou ↘) ; un gris, un jeton adverse ou une case vide l'interrompt.
- **Victoire de base modifiée** : un alignement d'**exactement 4** fait gagner (5 ou plus : voir Règle 4).
- **Fins de partie nulles ajoutées** : au coup n° 84 (2 × colonnes × lignes) sans vainqueur ; ou si la grille est pleine et que le joueur dont c'est le tour n'a aucun jeton sur la ligne du bas. **(v2)** Ces nuls ne s'appliquent que si le coup n'a fait ni gagner ni perdre : un 84e coup qui fait gagner (ou perdre) donne ce résultat, pas le match nul (Q2, cas 33).
- **(v2) Joueur en fin de partie** : si la partie se termine à `APRES_COUP` (victoire, défaite ou nul par priorités), `joueur` reste celui qui vient de jouer, car la main n'est pas passée. Si elle se termine par un nul de `FIN_DE_TOUR` (84 coups ou grille pleine), la main est déjà passée et `joueur` est l'adversaire (cas 27 et 35). La v1 ne le précisait pas ; le premier code passait la main avant de vérifier la victoire (cas 27, échec puis correction).

## Règle 1 — Pop out

**Catégorie :** placement

**Énoncé :** À son tour, au lieu de poser un jeton, un joueur peut retirer un de ses propres jetons situé sur la ligne du bas d'une colonne. Le jeton retiré sort du jeu et tous les jetons au-dessus de lui, gris compris, descendent d'une case. Ce retrait est le coup du joueur, puis c'est au tour de l'adversaire.

**Déclenchement :** À `AVANT_COUP` (le retrait est-il autorisé ?), à `PENDANT_COUP` (exécution du retrait à la place de la pose) et à `FIN_DE_TOUR` (match nul).

**Cas limite :** Si la colonne est vide ou si son jeton du bas est adverse ou gris, le coup est refusé. Si la grille est pleine, la partie n'est pas nulle tant que le joueur dont c'est le tour peut retirer un jeton. **(v2)** Un gris situé au-dessus du jeton retiré descend avec la pile ; arrivé sur la ligne du bas, il bloque le Pop out de cette colonne pour les deux joueurs (Q7, cas 32). La grille pleine sans aucun jeton en bas pour le joueur dont c'est le tour peut réellement se produire (ligne du bas d'un seul joueur, coupée par un gris) : match nul (Q6, cas 35). Un Pop out qui donne un alignement de 4 à l'adversaire le fait gagner (Q4, cas 20).

**Interagit avec :** gravité, Règle 2, Règle 3, Règle 4, Règle 5

**Hooks :** `AVANT_COUP` (autorise ou refuse le retrait), `PENDANT_COUP` (retire le jeton et fait descendre la pile), `FIN_DE_TOUR` (match nul : grille pleine, 84 coups)

## Règle 2 — Jeton gris

**Catégorie :** temporelle

**Énoncé :** Après chaque coup n° 15, 30, 45…, si la partie n'est pas finie, un jeton gris tombe automatiquement par gravité. Il tombe successivement dans la 2e, la 4e puis la 6e colonne (colonnes 1, 3, 5), puis la séquence recommence. Il ne compte pour aucun joueur et ne peut pas être retiré par Pop out.

**Déclenchement :** À `FIN_DE_TOUR`, juste après le changement de joueur ; la pose du gris n'est pas un coup et n'est pas ajoutée à `coups`.

**Cas limite :** Si la colonne prévue est pleine, le gris va dans la colonne suivante de la séquence, et si les colonnes 1, 3 et 5 sont pleines, aucun gris n'est posé. Le k-ième gris (après le coup n° 15·k) vise toujours la colonne `[1, 3, 5][(k-1) % 3]`. **(v2)** Un gris non posé ne décale pas la séquence : le suivant garde sa colonne prévue (Q3, cas 34). Si le coup n° 15·k fait gagner ou perdre, la partie est finie et aucun gris n'est posé (Q8, cas 31).

**Interagit avec :** gravité, Règle 1, Règle 3, Règle 4, Règle 5

**Hooks :** `FIN_DE_TOUR` (pose le gris après le coup n° 15, 30, 45…)

## Règle 3 — Carré

**Catégorie :** victoire

**Énoncé :** Un joueur qui a 4 de ses jetons formant un carré de 2 × 2 cases adjacentes gagne la partie. Le carré s'ajoute aux alignements gagnants (lignes, colonnes, diagonales).

**Déclenchement :** À `APRES_COUP`, vérifié pour les deux joueurs après chaque coup (pose ou Pop out).

**Cas limite :** Un carré qui contient un gris ou un jeton adverse ne compte pas. Si le même coup donne aussi 5 jetons alignés à ce joueur, il perd (Règle 4). **(v2)** Démontré par le cas 28 (Q1). Un coup qui forme à la fois un carré et un sandwich fait simplement gagner (cas 29).

**Interagit avec :** Règle 1, Règle 2, Règle 4, Règle 5

**Hooks :** `APRES_COUP` (« gagne » si carré)

## Règle 4 — Trop aligné

**Catégorie :** victoire

**Énoncé :** Un joueur qui a 5 jetons alignés ou plus perd la partie. Seul un alignement d'exactement 4 fait gagner.

**Déclenchement :** À `APRES_COUP`, en premier, vérifié pour les deux joueurs après chaque coup (pose ou Pop out).

**Cas limite :** Si un coup donne au même joueur une victoire et 5 jetons alignés, il perd. Si un Pop out donne 5 jetons alignés aux deux joueurs à la fois, la partie est nulle. **(v2)** Démontré par le cas 30 (Q5).

**Interagit avec :** Règle 1, Règle 2, Règle 3, Règle 5

**Hooks :** `APRES_COUP`, en premier (« perd » si 5 alignés ou plus)

## Règle 5 — Sandwich horizontal

**Catégorie :** victoire

**Énoncé :** Un joueur gagne s'il a, sur une même ligne horizontale, 5 cases consécutives contenant dans l'ordre 2 de ses jetons, 1 jeton adverse et 2 de ses jetons (`P P A P P`). Les motifs verticaux et diagonaux ne comptent pas.

**Déclenchement :** À `APRES_COUP`, vérifié pour les deux joueurs après chaque coup (pose ou Pop out).

**Cas limite :** Un gris au centre (`P P G P P`) ne forme pas de sandwich. Poser son jeton dans le trou d'un motif adverse `P P _ P P` fait gagner l'adversaire.

**Interagit avec :** gravité, Règle 1, Règle 2, Règle 3, Règle 4

**Hooks :** `APRES_COUP` (« gagne » si sandwich)

## Interactions déclarées
| Règles | Situation | Ce qui se passe |
|---|---|---|
| 1 et gravité | Pop out sous une pile de jetons | Toute la pile descend d'une case, gris compris ; la case du haut de la colonne devient vide. |
| 1 et 2 | Gris sur la ligne du bas | Il ne peut pas être retiré ; il bloque le Pop out de cette colonne pour les deux joueurs. |
| 1 et 2 | Pop out dans une colonne contenant un gris | Le gris descend d'une case comme les autres jetons. **(v2)** Cas 32 (Q7). |
| 1 et 2 | Comptage des coups | Un Pop out est un coup : il compte pour atteindre 15, 30, 45… |
| 1 et 3/4/5 | Un Pop out crée une configuration chez l'adversaire | Les deux joueurs sont évalués ; on applique l'ordre de priorité ci-dessous. Un Pop out peut donc faire gagner ou perdre l'adversaire. **(v2)** Cas 20 (Q4). |
| 1 et 3/4/5 | Un Pop out donne une victoire aux deux joueurs en même temps (sans alignement de 5 ou plus) | **Match nul** (priorité 4 de `APRES_COUP`). |
| 1 et 4 | Un Pop out donne un alignement de 5 ou plus aux deux joueurs en même temps | **Match nul** (priorité 1 de `APRES_COUP`). **(v2)** Cas 30 (Q5). |
| 1 et grille pleine | Plus de case libre | Pas nul tant que le joueur dont c'est le tour peut faire un Pop out ; nul sinon. **(v2)** Les deux situations sont possibles : cas 22 (la partie continue) et cas 35 (nul, Q6). |
| **(v2)** 1 et limite de 84 coups | Le 84e coup fait gagner ou perdre | Le résultat de `APRES_COUP` s'applique ; le nul de la limite n'est pas appliqué (Q2, cas 33). |
| 2 et 3/4/5 | Gris au milieu d'un motif | Il interrompt l'alignement, invalide le carré et n'est jamais le jeton « adverse » d'un sandwich. |
| 2 et fin de partie | Le 15e coup fait gagner ou perdre | La partie est finie : aucun gris n'est posé. **(v2)** Cas 31 (Q8). |
| **(v2)** 2 et colonnes pleines | Un gris est dû alors que les colonnes 1, 3 et 5 sont pleines | Aucun gris ; le gris suivant garde sa colonne prévue (Q3, cas 34). |
| 2 et 3/4/5 | Arrivée d'un gris | Elle ne peut créer aucun alignement, carré ou sandwich : elle ne fait ni gagner ni perdre. Si elle remplit la dernière case, on applique le match nul de `FIN_DE_TOUR`. |
| 3 et 4 | Un coup forme un carré et 5 alignés pour le même joueur | Défaite (la Règle 4 passe avant). **(v2)** Cas 28 (Q1). |
| 4 et 5 | Un coup forme un sandwich et 5 alignés pour le même joueur | Défaite (la Règle 4 passe avant). **(v2)** Cas 36 : les cinq alignés sont alors forcément en diagonale (un sandwich horizontal et cinq alignés sur la même ligne ne tiennent pas dans 7 colonnes). |
| 4 et base | Un coup forme un alignement de 4 et un autre de 5 ou plus | Défaite (la Règle 4 passe avant). |
| 3 et 5 | Un coup forme un carré et un sandwich | Victoire (même résultat, pas de conflit). **(v2)** Cas 29. |
| 5 et pose | Un joueur pose son jeton dans le trou d'un motif adverse `P P _ P P` | L'adversaire gagne (priorité 6 de `APRES_COUP`) ; si ce coup fait aussi gagner le poseur, match nul (priorité 4). |

## Ordre d'application général
Un coup se déroule toujours en **4 moments**, appelés **hooks**. À chaque hook, seules les règles qui y sont rattachées se déclenchent, dans l'ordre indiqué.

### Hook 1 — `AVANT_COUP` : le joueur a choisi son coup, rien n'a encore bougé
- **Base :** poser n'est autorisé que dans une colonne qui a une case libre.
- **Règle 1 :** autorise aussi le retrait d'un de ses propres jetons sur la ligne du bas ; refuse le retrait si la colonne est vide ou si son jeton du bas est adverse ou gris.
- Coup interdit → refusé (`ValueError`), rien ne change, on s'arrête là.

### Hook 2 — `PENDANT_COUP` : le coup est exécuté
- **Base :** le jeton posé tombe sur la case libre la plus basse.
- **Règle 1 :** le jeton retiré sort du jeu et la pile au-dessus descend d'une case, gris compris.
- Le compteur de coups augmente de 1.

### Hook 3 — `APRES_COUP` : le coup est joué, on regarde si la partie est finie
Les règles se déclenchent dans cet ordre, **pour les deux joueurs** :
1. **Règle 4** : un joueur qui a 5 jetons alignés ou plus « perd ».
2. **Base, Règle 3, Règle 5** : un joueur qui a 4 jetons alignés, un carré ou un sandwich « gagne ».

Soit A le joueur qui vient de jouer et B son adversaire. On applique **la première** ligne vraie :

| Priorité | Condition | Résultat |
|---|---|---|
| 1 | A **et** B perdent (5 alignés ou plus chacun) | nul |
| 2 | A perd | B gagne |
| 3 | B perd | A gagne |
| 4 | A **et** B gagnent | nul |
| 5 | A gagne | A gagne |
| 6 | B gagne | B gagne |

Si une ligne est vraie, la partie est finie et on s'arrête là. Après une **pose**, B ne peut « gagner » que par un sandwich (le jeton posé par A en est le centre) et ne peut jamais « perdre » : seules les priorités 2, 4, 5 et 6 sont alors possibles. Après un **Pop out**, les six priorités sont possibles. Comme chaque règle dit seulement « gagne » ou « perd » et que ce tableau tranche, l'ordre entre les règles 3 et 5 ne change pas le résultat.

**(v2)** « On s'arrête là » signifie que `FIN_DE_TOUR` n'a pas lieu : la main n'est pas passée (`joueur` reste A), aucun gris n'est posé et la limite de 84 coups n'est pas appliquée (Q2, Q8 ; cas 27, 31, 33).

### Hook 4 — `FIN_DE_TOUR` : la partie continue, on passe la main
Dans cet ordre :
1. **Base :** c'est au tour de B.
2. **Règle 2 :** si le numéro du coup est un multiple de 15, le jeton gris tombe (la pose du gris ne peut faire ni gagner ni perdre).
3. **Règle 1 :** la partie est nulle si le coup n° 84 (2 × colonnes × lignes) vient d'être joué, ou si la grille est pleine et que B n'a aucun jeton sur la ligne du bas. Une grille pleine n'est **pas** nulle tant que B peut retirer un jeton.

### Récapitulatif : quelle règle se déclenche à quel hook

| Règle | `AVANT_COUP` | `PENDANT_COUP` | `APRES_COUP` | `FIN_DE_TOUR` |
|---|---|---|---|---|
| R1 Pop out | ✓ autorise / refuse le retrait | ✓ retire et fait descendre la pile | | ✓ nul (grille pleine, 84 coups) |
| R2 Jeton gris | | | | ✓ pose le gris (coups n° 15, 30, 45…) |
| R3 Carré | | | ✓ « gagne » | |
| R4 Trop aligné | | | ✓ « perd » (en premier) | |
| R5 Sandwich | | | ✓ « gagne » | |

## Point d'accroche : réponses aux quatre questions de `moteur.py`

| Question | Réponse du groupe |
|---|---|
| À quel moment une règle intervient-elle ? | À un ou plusieurs des 4 hooks ci-dessus : avant le coup pour l'autoriser ou l'interdire (`AVANT_COUP`), pendant le coup pour déplacer des jetons (`PENDANT_COUP`), sur la victoire (`APRES_COUP`) ou au passage de la main (`FIN_DE_TOUR`). La Règle 1 se déclenche à trois hooks, les autres à un seul. |
| Une règle reçoit quoi, et rend quoi ? | Elle reçoit l'état sans jamais le modifier. À `PENDANT_COUP` et `FIN_DE_TOUR`, elle rend un **nouvel** état ; à `AVANT_COUP`, elle dit si le coup est autorisé ; à `APRES_COUP`, elle dit seulement « gagne » ou « perd » pour chaque joueur. |
| Dans quel ordre s'appliquent deux règles déclenchées au même tour ? | Dans l'ordre des hooks (1 → 4), puis, à l'intérieur d'un hook, dans l'ordre écrit ci-dessus (à `APRES_COUP` : Règle 4 d'abord, puis le tableau de priorités ; à `FIN_DE_TOUR` : changement de joueur, Règle 2, puis Règle 1). |
| Comment une règle à usage limité retient-elle qu'elle a servi ? | Ce serait dans l'état, mais aucune de nos règles n'est à usage limité : la séquence des gris se déduit du nombre de coups (`len(coups)`) et les gris posés sont dans `grille`. Rejouer la même liste de coups redonne donc toujours le même état. |

## Exemples de référence
Suites de coups vérifiables avec `rejouer()` (Pop out en colonne c noté `-(c+1)`) :

| Règle | Coups | Résultat attendu |
|---|---|---|
| 1 | `[0, 0, -1]` | X retire son jeton en colonne 0 : le O descend en ligne 5, colonne 0 ; partie en cours, au tour de O. |
| 1 | `[0, -1]` | O tente de retirer le X du bas de la colonne 0 → refusé, toujours au tour de O. |
| 1 + 3/4/5 | `[0, 0, 1, 1, 3, 2, 3, 2, 6, 3, -4]` | X retire en colonne 3 ; la pile descend et O aligne 4 sur la ligne 4 → **O gagne**. |
| 2 | `[0,0,0,0,0,0, 6,6,6,6,6,6, 2,2,2]` | Après le 15e coup, un gris tombe en ligne 5, colonne 1 ; partie en cours. |
| 2 + 1 | même suite + `[-2]` | O tente de retirer le gris en colonne 1 → refusé. |
| 3 | `[0, 6, 1, 6, 0, 5, 1]` | Carré X en colonnes 0–1, lignes 4–5 → **X gagne**. |
| 4 | `[0, 0, 1, 1, 3, 3, 4, 4, 2]` | X aligne 5 jetons en ligne 5 → **X perd, O gagne**. |
| 5 | `[0, 2, 1, 6, 3, 6, 4]` | Ligne 5 : `X X O X X` → **X gagne**. |
| 5 + pose | `[6, 0, 6, 1, 5, 3, 6, 4, 2]` | X pose au centre de `O O _ O O` en ligne 5 → **O gagne**. |
| **(v2)** 3 + 4 | `[2,0,3,1,0,4,1,5,3,6,4,5,2]` | Carré et 5 X alignés au même coup → **X perd, O gagne** (Q1). |
| **(v2)** 1 + 4 | `[0,1,2,0,3,2,1,3,4,1,6,4,6,-2]` | Le Pop out de O donne 5 alignés aux deux joueurs → **match nul** (Q5). |
| **(v2)** 2 + 3 | `[0,6,6,6,6,6,6,3,3,3,1,3,0,3,1]` | Le 15e coup fait gagner X par carré → **aucun gris** (Q8). |
| **(v2)** 1 + 2 | `[1,6,6,6,6,6,6,3,3,3,3,3,3,0,5,0,-2]` | Le Pop out de X fait descendre le gris en `[5][1]` ; O ne peut pas le retirer (Q7). |

Les suites longues des questions Q2, Q3 et Q6 (`V84`, `P60`, `N53`) sont recopiées dans `RECETTE.md` (cas 33 à 35).

## Changements depuis la v1

| Où | Changement | Origine |
|---|---|---|
| Conventions, fins nulles | Un 84e coup gagnant ou perdant donne ce résultat, pas le nul : **décision nouvelle**. | Q2, cas 33 |
| Conventions, joueur en fin de partie | Précision ajoutée : la main ne passe pas si la partie se termine à `APRES_COUP`. La v1 ne le disait pas ; le code d'origine passait la main trop tôt. | Cas 27 (échec puis correction) |
| Hook 3 | « On s'arrête là » explicité : ni passage de main, ni gris, ni limite de 84 coups. | Q2, Q8 ; cas 27, 31, 33 |
| Règle 1, cas limite | Gris descendu par un Pop out ; grille pleine sans jeton en bas, situation démontrée possible ; Pop out qui fait gagner l'adversaire. | Q7, Q6, Q4 ; cas 32, 35, 20 |
| Règle 2, cas limite | Un gris non posé ne décale pas la séquence ; pas de gris si le coup n° 15·k termine la partie. | Q3, Q8 ; cas 34, 31 |
| Règles 3 et 4 | Renvois aux démonstrations. | Q1, Q5 ; cas 28, 29, 30 |
| Interactions déclarées | Deux lignes ajoutées (limite de 84 coups, colonnes 1, 3, 5 pleines) ; renvois aux cas pour les autres ; précision géométrique pour « 4 et 5 ». | Q2, Q3 ; cas 36 |
| Exemples de référence | Quatre exemples ajoutés. | Cas 28, 30, 31, 32 |

Interactions déclarées encore sans cas de recette dédié (décisions de la v1 conservées) : « 2 et 3/4/5 » (gris au milieu d'un motif ; arrivée d'un gris qui remplit la dernière case), « 4 et base » (un alignement de 4 et un autre de 5 au même coup) et la variante nulle de « 5 et pose » (le poseur gagne aussi).
