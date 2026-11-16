# Cahier de recette — version 1

Rédigé le **13/11/2026**. Responsable du cahier dans le groupe : **Adnane BOUCHEHIT**.

Référence : `REGLEMENT-v1.md`. Les suites proviennent des exemples du règlement, des tests existants ou de préfixes de ces exemples. Ce cahier est rédigé **après le code et les tests récupérés dans l'archive** ; il ne constitue pas une preuve de rédaction avant leur développement. Les suites existantes avaient déjà été testées lors de l'intégration. Une nouvelle campagne a été exécutée par Codex le **13/11/2026** : **26 cas conformes aux attentes sur 26**, avec observations ci-dessous.

Vérification par appels Python aux fonctions du moteur, sans interface utilisateur, avec `-B` pour éviter les caches. Les états, motifs, résultats, refus et invariants mentionnés dans les attentes ont été contrôlés ; les suites longues ont été lues dans ce document. Aucun attendu n'a été changé après exécution. Ce résultat est limité aux cas présents : voir la couverture restant à compléter.

## Mode d'emploi

- Chaque cas repart d'une partie vide. Sauf mention **standard**, utiliser les cinq règles avec `rejouer(coups, REGLES)` ; consulter le résultat avant de changer les règles actives.
- Colonnes 0 à 6 ; ligne 0 en haut, ligne 5 en bas. Retirer en colonne `c` se note `-(c+1)`.
- « Puis tenter » signifie : rejouer le préfixe, conserver l'état obtenu, puis appeler `jouer()` avec le coup indiqué. Un refus doit lever `ValueError`, sans modifier l'état, le joueur ou l'historique.
- `S15`, `S30`, `DOUBLE`, `PLEINE`, `L84`, `V84`, `P60`, `N53` sont les listes exactes définies plus bas ; `[:n]` signifie leurs n premiers coups.
- À la vérification, renseigner l'état ou l'erreur réellement observés et la date dans **Observé**, puis ✓ ou ✗. Laisser ces colonnes vides tant que le cas n'a pas été vérifié dans cette campagne. Une partie en cours signifie `gagnant(...) == None` et `fini == False`.
- Les attentes sont à relire en groupe ; un écart doit être expliqué, pas effacé en adaptant l'attendu au code. Ne pas modifier la v1 remise au professeur.

## Cas à vérifier

| N° | Règle / objectif | Coups joués / procédure | Attendu | Observé | ✓/✗ | Écrit le |
|---|---|---|---|---|---|---|
| 01 | Base : gravité et empilement | Standard : `[3,3]` | X en `[5][3]`, O en `[4][3]` ; à X de jouer, tour 3 ; partie en cours. | 13/11/2026 : X en [5][3], O en [4][3] ; joueur X, tour 3 ; aucun gagnant, fini=False. | ✓ | 13/11/2026 |
| 02 | Base : alignement | Standard : `[0,0,1,1,2,2,3]` | X gagne horizontalement ; `fini=True`, aucun coup possible. | 13/11/2026 : Quatre X en ligne 5 ; gagnant X, fini=True, coups possibles []. | ✓ | 13/11/2026 |
| 03 | Base : match nul | Standard : `nouvelle_partie(colonnes=3, lignes=1)`, puis jouer `[0,1,2]` | Grille pleine sans alignement : `nul`, `fini=True`. Aucun gris ni Pop out en mode standard. | 13/11/2026 : Grille [[X,O,X]] ; résultat nul, fini=True ; aucun gris. | ✓ | 13/11/2026 |
| 04 | R1 : retrait autorisé, gravité | `[0,0,-1]` | O descend en `[5][0]`, `[4][0]` devient vide ; à O de jouer ; partie en cours. | 13/11/2026 : O en [5][0], [4][0] vide ; joueur O, tour 4 ; partie en cours. | ✓ | 13/11/2026 |
| 05 | R1 : jeton adverse | `[0]`, puis tenter `-1` | Refus : O ne peut pas retirer le X du bas ; état inchangé, toujours à O. | 13/11/2026 : ValueError : coup illegal : -1 ; état intégralement inchangé, joueur O. | ✓ | 13/11/2026 |
| 06 | R1 : colonne vide | `[]`, puis tenter `-4` | Refus du retrait en colonne 3 ; état vide inchangé, toujours à X. | 13/11/2026 : ValueError : coup illegal : -4 ; état intégralement inchangé, joueur X. | ✓ | 13/11/2026 |
| 07 | Base + R1 : colonne pleine | `[2,2,2,2,2,2]`, puis tenter `2` | Pose refusée, colonne 2 absente des poses possibles ; retrait `-3` autorisé pour X, qui possède le jeton du bas. | 13/11/2026 : ValueError : coup illegal : 2 ; état inchangé ; coups possibles [0,1,3,4,5,6,-3], joueur X. | ✓ | 13/11/2026 |
| 08 | R2 : premier gris | `S15` | Gris en `[5][1]` après le coup 15 ; exactement 15 coups dans l'historique ; à O de jouer ; partie en cours. | 13/11/2026 : Gris en [5][1] ; historique égal à S15 (15 coups), joueur O ; partie en cours. | ✓ | 13/11/2026 |
| 09 | R2 : aucun déclenchement anticipé | `S15[:14]` | Aucun gris ; 14 coups ; partie en cours. | 13/11/2026 : Aucun gris après 14 coups ; gagnant None, fini=False. | ✓ | 13/11/2026 |
| 10 | R2 : colonne prévue pleine | `[1,1,1,1,1,1,0,0,0,0,0,0,6,6,6]` | Au coup 15, colonne 1 pleine : gris en `[5][3]` ; partie en cours. | 13/11/2026 : Colonne 1 pleine ; gris en [5][3] au coup 15 ; partie en cours. | ✓ | 13/11/2026 |
| 11 | R2 + R1 : retraits comptés, deuxième gris | `S30` | 30 coups, retraits compris ; le gris du coup 30 tombe en colonne 3 ; partie en cours. | 13/11/2026 : 30 coups ; un gris supplémentaire au dernier coup, en [4][3] ; autre gris en [5][1] ; partie en cours. | ✓ | 13/11/2026 |
| 12 | R2 + R1 : gris non retirable | `S15`, puis tenter `-2` | Refus : le jeton du bas de la colonne 1 est gris ; état inchangé. | 13/11/2026 : ValueError : coup illegal : -2 ; gris en [5][1], état inchangé. | ✓ | 13/11/2026 |
| 13 | R3 : carré gagnant | `[0,6,1,6,0,5,1]` | Carré X aux lignes 4–5, colonnes 0–1 : X gagne et la partie finit. | 13/11/2026 : Carré X aux lignes 4–5 et colonnes 0–1 ; gagnant X, fini=True. | ✓ | 13/11/2026 |
| 14 | R3 : carré incomplet | `[0,6,1,6,0,5]` | Il manque le X en `[4][1]` ; aucun carré gagnant, partie en cours. | 13/11/2026 : [4][1] vide ; gagnant None, fini=False. | ✓ | 13/11/2026 |
| 15 | R4 : cinq alignés | `[0,0,1,1,3,3,4,4,2]` | X forme cinq jetons horizontaux : X perd, O gagne ; partie finie. | 13/11/2026 : Cinq X consécutifs en ligne 5 ; gagnant O, fini=True. | ✓ | 13/11/2026 |
| 16 | R4 : quatre ne font pas perdre | `[3,4,3,4,3,4,3]` | Exactement quatre X verticaux : X gagne, sans défaite pour trop d'alignement. | 13/11/2026 : Quatre X verticaux en colonne 3 ; gagnant X, fini=True. | ✓ | 13/11/2026 |
| 17 | R5 : sandwich gagnant | `[0,2,1,6,3,6,4]` | Ligne 5, colonnes 0–4 : `X X O X X` ; X gagne. | 13/11/2026 : Motif X X O X X en ligne 5, colonnes 0–4 ; gagnant X, fini=True. | ✓ | 13/11/2026 |
| 18 | R5 : sandwich incomplet | `[0,2,1,6,3,6]` | Case `[5][4]` vide : aucun sandwich gagnant ; partie en cours. | 13/11/2026 : [5][4] vide ; gagnant None, fini=False. | ✓ | 13/11/2026 |
| 19 | R5 + pose adverse | `[6,0,6,1,5,3,6,4,2]` | X complète le centre du motif `O O X O O` : O gagne. | 13/11/2026 : Motif O O X O O en ligne 5, colonnes 0–4 ; gagnant O, fini=True. | ✓ | 13/11/2026 |
| 20 | R1 + victoire adverse | `[0,0,1,1,3,2,3,2,6,3,-4]` | Le retrait de X fait descendre la pile ; O aligne quatre en ligne 4 et gagne. | 13/11/2026 : Quatre O en ligne 4, colonnes 0–3 ; gagnant O après le retrait, fini=True. | ✓ | 13/11/2026 |
| 21 | R1 + victoires simultanées | `DOUBLE` | Après le dernier Pop out, les deux joueurs gagnent sans cinq alignés : priorité 4, match nul et partie finie. | 13/11/2026 : Après 53 coups : alignement maximal de 4 pour X et pour O, aucun de 5 ; résultat nul, fini=True. | ✓ | 13/11/2026 |
| 22 | R1 + R2 : grille pleine | `PLEINE` | Grille pleine, sans vainqueur ; un Pop out reste possible pour le joueur courant : partie en cours, coups possibles non vides et tous négatifs. | 13/11/2026 : Toutes les cases occupées après 40 coups ; joueur X, coups possibles [-3,-5,-6] ; gagnant None, fini=False. | ✓ | 13/11/2026 |
| 23 | R1 : limite de durée | `L84[:83]`, puis jouer le dernier coup de `L84` | Après 83 coups : partie en cours. Après 84 : match nul, partie finie. | 13/11/2026 : 83 coups : gagnant None, fini=False. 84 coups : résultat nul, fini=True, aucun coup possible. | ✓ | 13/11/2026 |
| 24 | R1 : immutabilité | Préparer `[0,0]`, garder une copie de l'état, puis jouer `-1` | L'ancien état garde X sous O et deux coups. Le nouvel état contient O seul en colonne 0 et l'historique `[0,0,-1]`. | 13/11/2026 : Ancien état égal à sa copie : X sous O, historique [0,0]. Nouvel état : O seul en colonne 0, historique [0,0,-1]. | ✓ | 13/11/2026 |
| 25 | R1 : reproductibilité | `[0,0,-1,3,3,-4]`, par `rejouer` puis par appels successifs à `jouer`, mêmes règles actives | Les deux états complets sont égaux, dont grille, historique, joueur, tour et fin de partie. | 13/11/2026 : Égalité complète des deux dictionnaires après les six coups ; joueur X, tour 7, fini=False. | ✓ | 13/11/2026 |
| 26 | R3 + fin de partie | `[0,6,1,6,0,5,1]`, puis tenter `3` | X a déjà gagné par carré : tout nouveau coup est refusé, état terminal inchangé. | 13/11/2026 : ValueError : coup illegal : 3 ; état terminal inchangé, gagnant X, fini=True. | ✓ | 13/11/2026 |

## Cas complémentaire — arrêt avant le passage de main

Ajouté le 16/11/2026, avant toute correction du moteur. Référence : `APRES_COUP` arrête la partie avant `FIN_DE_TOUR` dans le règlement v1.

| N° | Procédure | Attendu | Observé | Verdict |
|---|---|---|---|---|
| 27 | Rejouer `[0,6,1,6,0,5]` avec `REGLES`, puis jouer `1`. | Avant : joueur X, partie en cours. Après : carré gagnant de X, `fini=True`, `joueur='X'` conservé ; historique de sept coups. | 16/11/2026 : avant, joueur X et aucun gagnant ; après, gagnant X et fini=True, mais joueur O. | Échec : passage de main prématuré. |

Après correction autorisée, nouvelle vérification le 16/11/2026 : joueur X conservé, gagnant X, fini=True, historique de sept coups ; état précédent inchangé et rejeu identique. **Cas 27 conforme.** L'échec initial ci-dessus est conservé pour tracer le diagnostic.

Ce contrôle s'ajoute aux 26 cas historiques ; la campagne complète des 26 cas n'a pas été réexécutée. Les 16 tests du socle, les 21 tests des règles et les trois tests complémentaires de `test_fin_partie.py` passent.

## Cas d'interaction ajoutés

Attendus écrits à partir de `REGLEMENT-v1.md` (cas limites des règles, section « Interactions déclarées », tableau de priorités de `APRES_COUP`), avant toute exécution de chaque cas.

| N° | Règle / objectif | Coups joués / procédure | Attendu | Observé | ✓/✗ | Écrit le |
|---|---|---|---|---|---|---|
| 28 | R3 + R4 : carré et cinq alignés au même coup | `[2,0,3,1,0,4,1,5,3,6,4,5,2]` ; contrôler aussi le préfixe de 12 coups | Après 12 coups : ligne 4 `X X . X X O .`, ligne 5 `O O X X O O O`, aucun gris, partie en cours. Après le 13e coup (X en `[4][2]`) : cinq X en ligne 4 (colonnes 0–4) et carré X `[4][2]`, `[4][3]`, `[5][2]`, `[5][3]`. R4 passe avant : X perd, **O gagne**, `fini=True`, joueur X conservé, historique de 13 coups. | 16/11/2026 : après 12 coups, ligne 4 `X X . X X O .`, ligne 5 `O O X X O O O`, aucun gris, gagnant None, fini=False, joueur X. Après 13 coups : ligne 4 `X X X X X O .` ; gagnant O, fini=True, joueur X, 13 coups. Préfixe inchangé ; `rejouer` donne le même état. | ✓ | 16/11/2026 |
| 29 | R3 + R5 : carré et sandwich au même coup | `[2,0,3,1,4,5,0,2,1,6,3,5,4]` ; contrôler aussi le préfixe de 12 coups | Après 12 coups : ligne 4 `X X O X . O .`, ligne 5 `O O X X X O O`, aucun gris, partie en cours. Après le 13e coup (X en `[4][4]`) : sandwich X en ligne 4 (`X X O X X`, colonnes 0–4) et carré X `[4][3]`, `[4][4]`, `[5][3]`, `[5][4]` ; aucun alignement de cinq. Pas de conflit (priorité 5) : **X gagne**, `fini=True`, joueur X conservé, historique de 13 coups. | 16/11/2026 : après 12 coups, ligne 4 `X X O X . O .`, ligne 5 `O O X X X O O`, aucun gris, gagnant None, fini=False, joueur X. Après 13 coups : ligne 4 `X X O X X O .` ; gagnant X, fini=True, joueur X, 13 coups. Préfixe inchangé ; `rejouer` donne le même état. | ✓ | 16/11/2026 |
| 30 | R1 + R4 : deux défaites simultanées après un Pop out | `[0,1,2,0,3,2,1,3,4,1,6,4,6,-2]` ; contrôler aussi le préfixe de 13 coups | Après 13 coups : ligne 3 `. O . . . . .`, ligne 4 `O X O O O . X`, ligne 5 `X O X X X . X`, aucun gris, partie en cours, à O de jouer. Après le 14e coup (O retire en colonne 1) : ligne 4 `O O O O O . X`, ligne 5 `X X X X X . X` ; les deux joueurs ont cinq alignés. Priorité 1 : **match nul**, `fini=True`, joueur O conservé, historique de 14 coups. | 16/11/2026 : après 13 coups, lignes 3–5 conformes, aucun gris, gagnant None, fini=False, joueur O. Après 14 coups : ligne 3 vide, ligne 4 `O O O O O . X`, ligne 5 `X X X X X . X` ; résultat nul, fini=True, joueur O, 14 coups, aucun gris. Préfixe inchangé ; `rejouer` donne le même état. | ✓ | 16/11/2026 |
| 31 | Q8 — R2 + R3 : le 15e coup fait gagner, aucun gris | `[0,6,6,6,6,6,6,3,3,3,1,3,0,3,1]` ; contrôler aussi le préfixe de 14 coups | Après 14 coups : ligne 4 `X . . X . . X`, ligne 5 `X X . O . . O`, aucun gris, partie en cours, à X de jouer. Après le 15e coup (X en `[4][1]`) : carré X `[4][0]`, `[4][1]`, `[5][0]`, `[5][1]` ; **X gagne**, `fini=True` ; **aucun gris** sur la grille ; joueur X conservé, historique de 15 coups. | 16/11/2026 : après 14 coups, ligne 4 `X . . X . . X`, ligne 5 `X X . O . . O`, aucun gris, gagnant None, fini=False, joueur X. Après 15 coups : ligne 4 `X X . X . . X` ; gagnant X, fini=True, joueur X, 15 coups, 0 gris sur la grille. Préfixe inchangé ; `rejouer` donne le même état. | ✓ | 16/11/2026 |
| 32 | Q7 — R1 + R2 : un Pop out retire le jeton sous un gris | `[1,6,6,6,6,6,6,3,3,3,3,3,3,0,5,0,-2]`, puis tenter `-2` ; contrôler aussi le préfixe de 15 coups | Après 15 coups : gris en `[4][1]` au-dessus du X en `[5][1]`, partie en cours. Après 17 coups (X retire en colonne 1) : gris descendu en `[5][1]`, `[4][1]` vide, ligne 5 `O G . O . X O`, un seul gris, partie en cours, à O de jouer, 17 coups. Puis `-2` absent des coups possibles de O ; tenter `-2` lève `ValueError`, état inchangé. | 16/11/2026 : après 15 coups, G en [4][1] et X en [5][1], gagnant None, fini=False. Après 17 coups : ligne 5 `O G . O . X O`, [4][1] vide, 1 gris, gagnant None, fini=False, joueur O, 17 coups. Coups possibles de O : [0,1,2,4,5,-1,-4,-7], sans -2 ; ValueError : coup illegal : -2 ; état inchangé ; `rejouer` donne le même état. | ✓ | 16/11/2026 |
| 33 | Q2 — R1 + R3 : le 84e coup fait gagner | `V84` ; contrôler aussi `V84[:83]` | Après 83 coups : partie en cours, à O de jouer ; lignes 3 `O X . O . G .` et 4 `X O . O O O X`. Après le 84e coup (O en `[3][4]`) : carré O `[3][3]`, `[3][4]`, `[4][3]`, `[4][4]`. La victoire passe avant la limite de 84 coups : **O gagne** (pas de match nul), `fini=True`, joueur O conservé, historique de 84 coups. | 16/11/2026 : après 83 coups, lignes 3 et 4 conformes, gagnant None, fini=False, joueur O. Après 84 coups : ligne 3 `O X . O O G .` ; gagnant O (pas nul), fini=True, joueur O, 84 coups. Préfixe inchangé ; `rejouer` donne le même état. | ✓ | 16/11/2026 |
| 34 | Q3 — R2 : gris dus alors que les colonnes 1, 3 et 5 sont pleines | `P60` ; contrôler les états après 15, 30, 45 et 60 coups | Coup 15 (1er gris, vise la colonne 1) : colonne 1 pleine, le gris va en colonne 3. Coups 30 et 45 : colonnes 1, 3 et 5 pleines, **aucun gris** posé ; toujours un seul gris sur la grille. Coup 60 (4e gris) : il garde sa colonne prévue `[1,3,5][(4-1) % 3]` = **colonne 1**, et tombe en `[1][1]` alors que la colonne 5 est libre ; deux gris au total. Partie en cours à chaque étape ; à X de jouer après 60 coups. | 16/11/2026 : 14 coups, aucun gris ; 15 coups, colonne 1 pleine, gris en [2][3]. 29 et 30 coups : colonnes 1, 3, 5 pleines, un seul gris (descendu en [4][3] par un retrait). 44 et 45 coups : colonnes pleines, un seul gris (en [5][3]). 59 coups : colonnes 1 et 5 libres ; 60 coups : nouveau gris en [1][1], deux gris au total. Gagnant None et fini=False à chaque étape ; joueur X après 60 coups. `rejouer` égal à la suite d'appels à `jouer`. | ✓ | 16/11/2026 |
| 35 | Q6 — R1 + R2 : grille pleine, le joueur suivant n'a aucun jeton en bas | `N53` ; contrôler aussi `N53[:52]` | Après 52 coups : partie en cours, à X de jouer, seule la case `[0][3]` est vide ; ligne 5 `X X X G X X X`. Après le 53e coup (X en `[0][3]`) : grille pleine, aucun alignement de quatre, carré ni sandwich ; O n'a aucun jeton sur la ligne du bas, il ne peut ni poser ni retirer : **match nul**, `fini=True`, aucun coup possible. Le nul est vérifié à `FIN_DE_TOUR`, après le passage de main : joueur **O** ; historique de 53 coups. | 16/11/2026 : après 52 coups, seule [0][3] vide, ligne 5 `X X X G X X X`, gagnant None, fini=False, joueur X. Après 53 coups : aucune case vide ; résultat nul, fini=True, joueur O, 53 coups, coups possibles []. Préfixe inchangé ; `rejouer` donne le même état. | ✓ | 16/11/2026 |
| 36 | R4 + R5 (+ R1) : sandwich et cinq alignés au même coup | `[6,2,2,3,-7,0,3,0,5,4,1,0,6,1,5,4,0,5,-7,1,5,3,5,2,6,0,3,-4]` ; contrôler aussi le préfixe de 27 coups | Après 27 coups : partie en cours, à O de jouer, gris en `[3][1]`. Après le 28e coup (O retire en colonne 3) : sandwich O en ligne 4 (`O O X O O`, colonnes 0–4) et cinq O en diagonale `[1][0]`, `[2][1]`, `[3][2]`, `[4][3]`, `[5][4]`. La Règle 4 passe avant : O perd, **X gagne**, `fini=True`, joueur O conservé, historique de 28 coups. | 16/11/2026 : après 27 coups, G en [3][1], gagnant None, fini=False, joueur O. Après 28 coups : ligne 4 `O O X O O X .`, diagonale O de [1][0] à [5][4] ; gagnant X, fini=True, joueur O, 28 coups. Préfixe inchangé ; `rejouer` donne le même état. | ✓ | 16/11/2026 |

## Suites longues reprises des tests existants

```python
S15 = [0,0,0,0,0,0,6,6,6,6,6,6,2,2,2]

S30 = [3,3,4,3,1,2,-2,-3,3,6,-5,-7,-4,-4,5,0,4,-1,-6,4,
       -5,-5,2,-4,3,0,-3,-1,-4,6]

DOUBLE = [3,3,0,4,2,5,-4,-4,1,2,0,-6,-2,0,-1,1,4,-5,-5,0,-3,5,
          6,6,-1,4,3,-6,2,4,-7,0,0,-1,6,3,5,2,1,4,4,1,3,-3,5,
          -5,2,4,4,5,6,-5,-4]

PLEINE = [4,0,0,6,4,3,0,3,2,1,0,0,3,1,3,2,0,2,3,2,5,3,2,4,2,
          5,1,1,6,4,5,1,4,5,4,6,5,6,6,6]

L84 = S30 + [-4,-7,3,5,4,-6,-5,2,0,-3,3,2,-1,-3,2,2,6,3,-7,5,
             5,4,-3,-3,2,-5,-3,0,6,-1,-7,0,5,-1,2,5,4,5,-5,0,
             -3,2,6,-3,-7,-1,4,2,-5,-3,4,6,2,-7]

V84 = [3,5,3,0,4,3,1,3,3,2,1,5,3,-1,1,1,1,6,-4,3,6,2,-5,0,0,4,5,-5,-2,0,
       6,5,2,1,6,-3,-4,3,2,-6,0,0,-2,0,-2,1,1,-7,5,-3,-7,-4,6,6,-3,4,-3,-6,
       -7,-4,3,5,-6,-5,-4,3,-7,4,-7,-5,2,5,-3,-7,4,4,-5,4,6,2,-7,6,6,4]

P60 = [5,1,1,3,5,1,5,5,1,5,3,1,1,5,3,3,3,-4,3,2,-6,2,5,2,-4,3,2,6,4,2,
       -5,6,2,6,6,0,6,-1,6,4,-4,3,0,-7,0,-5,-1,-2,-6,-7,-2,-7,4,5,-7,6,-6,0,6,-6]

N53 = [4,2,4,0,0,3,6,2,4,0,1,1,6,1,6,6,1,6,2,5,2,6,5,2,1,-1,2,5,0,-4,
       5,4,4,4,0,5,0,0,5,-6,5,-3,3,3,-7,2,6,-3,2,3,-7,6,3]
```

`V84`, `P60` et `N53` ont été trouvées le 16/11/2026 par un script de recherche écrit d'après le règlement v1, indépendant de `moteur.py` et `regles.py` (hors dépôt) ; les attendus des cas 33, 34 et 35 viennent des décisions Q2, Q3 et Q6 de `QUESTIONS.md`, pas du moteur. La suite du cas 36 a été trouvée par le même script ; son attendu vient de l'interaction « 4 et 5 » du règlement v1.

## Couverture à compléter

État au 16/11/2026 : 36 cas, tous conformes (le cas 27 a d'abord échoué, puis été corrigé). Chaque règle a au moins un déclenchement et un non-déclenchement ou refus. Les cas 28 à 36 couvrent les interactions R3/R4, R3/R5, R4/R5, la double défaite après Pop out, la descente d'un gris après retrait, l'absence de gris quand le 15e coup finit la partie, les colonnes cibles pleines, la grille pleine sans Pop out possible et la victoire au 84e coup ; ils servent aussi de démonstrations à `QUESTIONS.md`.

Restent sans cas dédié (décisions du règlement inchangées) :

- « 2 et 3/4/5 » : gris au milieu d'un motif (`P P G P P`, carré ou alignement coupé par un gris) ; arrivée d'un gris qui remplit la dernière case.
- « 4 et base » : un même coup forme un alignement de 4 et un autre de 5 ou plus.
- « 5 et pose », variante nulle : le poseur complète le sandwich adverse et gagne aussi (une suite existe dans `test_reglement.py`).
- Cas limites de R5 non couverts : motifs verticaux et diagonaux, qui ne doivent pas faire gagner.

Selon l'enseignant (séance 4), dépasser 30 cas est possible sans abuser. Ne pas considérer le nombre de lignes comme une preuve de couverture. L'ordre du changement de joueur au coup terminal est corrigé et vérifié par le cas 27 : voir `SUIVI.md`.
