# Cahier de recette — version 1

Rédigé le **13/11/2026**. Responsable du cahier dans le groupe : **Adnane BOUCHEHIT**.

Référence : `REGLEMENT-v1.md`. Les suites proviennent des exemples du règlement, des tests existants ou de préfixes de ces exemples. Ce cahier est rédigé **après le code et les tests récupérés dans l'archive** ; il ne constitue pas une preuve de rédaction avant leur développement. Les suites existantes avaient déjà été testées lors de l'intégration. Une nouvelle campagne a été exécutée par Codex le **13/11/2026** : **26 cas conformes aux attentes sur 26**, avec observations ci-dessous.

Vérification par appels Python aux fonctions du moteur, sans interface utilisateur, avec `-B` pour éviter les caches. Les états, motifs, résultats, refus et invariants mentionnés dans les attentes ont été contrôlés ; les suites longues ont été lues dans ce document. Aucun attendu n'a été changé après exécution. Ce résultat est limité aux cas présents : voir la couverture restant à compléter.

## Mode d'emploi

- Chaque cas repart d'une partie vide. Sauf mention **standard**, utiliser les cinq règles avec `rejouer(coups, REGLES)` ; consulter le résultat avant de changer les règles actives.
- Colonnes 0 à 6 ; ligne 0 en haut, ligne 5 en bas. Retirer en colonne `c` se note `-(c+1)`.
- « Puis tenter » signifie : rejouer le préfixe, conserver l'état obtenu, puis appeler `jouer()` avec le coup indiqué. Un refus doit lever `ValueError`, sans modifier l'état, le joueur ou l'historique.
- `S15`, `S30`, `DOUBLE`, `PLEINE`, `L84` sont les listes exactes définies plus bas ; `[:n]` signifie leurs n premiers coups.
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
```

## Couverture à compléter

Cette première version contient 26 cas et au moins un déclenchement et un non-déclenchement/refus pour chacune des cinq règles. Elle ne couvre pas encore toutes les interactions et tous les cas limites :

- Priorités R3/R4, R4/R5 et victoire simultanée R3/R5 ; deux défaites simultanées après Pop out.
- Gris interrompant explicitement les motifs de R3/R4/R5, descente d'un gris après retrait ; absence de gris lorsqu'un coup multiple de 15 finit la partie ; trois colonnes cibles pleines.
- Grille pleine sans Pop out possible ; motifs verticaux/diagonaux non gagnants pour R5 et centre gris.

Compléter ou regrouper les cas avec le groupe pour respecter la couverture demandée (chaque interaction déclarée et chaque cas limite), tout en visant 20 à 30 cas. Ne pas considérer le nombre de lignes comme une preuve de couverture. L'ordre du changement de joueur au coup terminal reste à clarifier : voir `SUIVI.md`.
