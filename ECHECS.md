# Trois échecs rencontrés pendant le travail avec l’IA

Groupe : Rayhan DAHMANI, Adnane BOUCHEHIT, Adam ZEKARI, Valentin PREVOT.
Rédigé le 20/11/2026.

## Échec 1 — Passer la main alors que le coup termine la partie

**Ce qu’on avait demandé — reconstitution :** implémenter le moteur et les règles en respectant les quatre étapes du règlement : autoriser le coup, l’exécuter, vérifier les victoires et défaites, puis passer la main seulement si la partie continue.

**Ce qui a été livré :** le moteur récupéré dans l’archive passait la main avant de vérifier la victoire. La suite `[0,6,1,6,0,5,1]` faisait gagner X par carré, mais l’état final indiquait O comme joueur. Le code du commit `3e3bf44` confirme cet ordre incorrect. Le défaut du code est établi ; faute d’échange de génération, son attribution précise à l’IA n’est pas vérifiable dans le dépôt.

**Comment on l’a remarqué :** le cas 27 de la recette comparait le joueur avant et après le coup gagnant. Avant le dernier coup, X devait jouer ; après ce coup, le résultat était bien X et `fini=True`, mais `joueur` valait O. Le règlement arrêtait pourtant le traitement avant `FIN_DE_TOUR`. L’échec initial du 16/11/2026 reste inscrit dans la recette.

**Ce qu’on a changé dans la demande — précision rétrospective proposée :** préciser explicitement le moment du passage de main et donner un état attendu : « Après `[0,6,1,6,0,5,1]`, X gagne, `fini=True` et `joueur='X'`. Ne passe la main que si la vérification des victoires n’a pas terminé la partie. Vérifie aussi une victoire de O et une victoire de l’adversaire après retrait. » La correction effectivement enregistrée dans `9f8556d` déplace le passage de main à `FIN_DE_TOUR` et adapte l’identification du dernier joueur à la parité de l’historique.

## Échec 2 — Tester une victoire de O après une victoire déjà acquise par X

**Ce qu’on avait demandé — reconstitution :** vérifier la correction du joueur terminal avec plusieurs situations, notamment une victoire de X et une victoire de O, sans modifier le règlement ni les signatures du moteur.

**Ce qui a été livré :** une première suite de test censée faire gagner O donnait déjà un carré gagnant à X au coup précédent. Le test cherchait donc à jouer après la fin de la partie. Le suivi conserve cette erreur ; la suite initiale exacte n’a pas été conservée dans le dépôt.

**Comment on l’a remarqué :** le moteur refusait le coup suivant. En examinant le préfixe de la suite, le carré de X expliquait ce refus : le moteur avait raison, c’était le scénario de test qui était incorrect. Le suivi du 16/11/2026 décrit le remplacement des coups de X puis la réussite du test, sans modification du moteur pour contourner le refus.

**Ce qu’on a changé dans la demande — précision rétrospective proposée :** demander de contrôler les étapes précédant le résultat : « Construis une suite qui fait gagner O uniquement au dernier coup. Vérifie que chaque préfixe reste en cours, sans victoire de X ni de O. Si un préfixe termine déjà la partie, corrige la suite de test, pas le moteur. » La suite corrigée présente dans `test_fin_partie.py` est `[6,0,6,1,4,0,3,1]` ; elle vérifie aussi que le joueur terminal reste celui qui vient de jouer.

## Échec 3 — Annoncer une couverture complète sans vérifier chaque interaction

**Ce qu’on avait demandé — reconstitution :** compléter la recette avec le cas où un même coup forme un sandwich et cinq jetons alignés, puis mettre à jour la documentation des interactions couvertes.

**Ce qui a été livré :** après le cas 36, une première rédaction affirmait que toutes les interactions déclarées avaient un cas de recette. Plusieurs situations restaient pourtant absentes : gris dans un motif, gris remplissant la dernière case, alignements de quatre et cinq simultanés et double victoire après une pose complétant un sandwich adverse.

**Comment on l’a remarqué :** la comparaison ligne par ligne du tableau des interactions avec la recette a révélé ces lacunes. Le suivi de séance 4 indique explicitement que l’affirmation était fausse et qu’elle a été corrigée immédiatement. La version enregistrée au commit `6995fc3` mentionne déjà les interactions restantes ; elle ne contient pas la rédaction erronée initiale.

**Ce qu’on a changé dans la demande — précision rétrospective proposée :** remplacer une appréciation générale par une correspondance vérifiable : « Pour chaque interaction déclarée dans le règlement, indique le numéro du cas qui la vérifie. Si aucun cas ne correspond, écris qu’elle reste à tester. Ne conclus pas que la couverture est complète à partir du seul nombre de tests réussis. » La correction historique a rétabli la liste des lacunes ; le tableau de correspondance et les cas 37 à 43 ont ensuite été ajoutés à la recette le 20/11/2026.

Sources : `SUIVI.md` (diagnostic et correction du joueur terminal, préparation de la séance 4), `RECETTE.md` (cas 27 et couverture), `test_fin_partie.py` et commits `3e3bf44`, `9f8556d`, `6995fc3`.
