"""Regression : arret APRES_COUP avant le passage de main (recette 27).

Lancement : python -B -m unittest test_fin_partie -v
"""
from copy import deepcopy
import unittest

import moteur as M
from regles import REGLES


class FinPartieTests(unittest.TestCase):
    def tearDown(self):
        M.activer_regles()

    def test_arret_avant_passage_de_main(self):
        cas = [
            ([0, 6, 1, 6, 0, 5, 1], REGLES, "X"),  # carre
            ([6, 0, 6, 1, 4, 0, 3, 1], REGLES, "O"),  # carre O
            ([0, 0, 1, 1, 3, 3, 4, 4, 2], REGLES, "O"),  # defaite X
            ([6, 0, 6, 1, 5, 3, 6, 4, 2], REGLES, "O"),  # sandwich adverse
            ([0, 0, 1, 1, 3, 2, 3, 2, 6, 3, -4], REGLES, "O"),
            ([0, 0, 1, 1, 2, 2, 3], None, "X"),  # standard
        ]
        for coups, regles, resultat in cas:
            with self.subTest(coups=coups):
                avant = M.rejouer(coups[:-1], regles)
                copie = deepcopy(avant)
                apres = M.jouer(avant, coups[-1])
                self.assertEqual(avant, copie)
                self.assertEqual(apres["joueur"], avant["joueur"])
                self.assertTrue(apres["fini"])
                self.assertEqual(M.gagnant(apres), resultat)
                self.assertEqual(apres["coups"], coups)
                self.assertEqual(M.coups_possibles(apres), [])
                self.assertEqual(apres, M.rejouer(coups, regles))
                terminal = deepcopy(apres)
                with self.assertRaises(ValueError):
                    M.jouer(apres, 3)
                self.assertEqual(apres, terminal)

    def test_continuation_passe_la_main(self):
        etat = M.rejouer([0, 0, -1], REGLES)
        self.assertFalse(etat["fini"])
        self.assertEqual(etat["joueur"], "O")

    def test_nul_fin_de_tour_passe_la_main(self):
        M.activer_regles()
        etat = M.nouvelle_partie(colonnes=3, lignes=1)
        for coup in [0, 1, 2]:
            etat = M.jouer(etat, coup)
        self.assertTrue(etat["fini"])
        self.assertEqual(M.gagnant(etat), "nul")
        self.assertEqual(etat["joueur"], "O")


if __name__ == "__main__":
    unittest.main()
