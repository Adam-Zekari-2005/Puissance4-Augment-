"""Contrôles des outils terminal de la séance 5."""
import contextlib
import io
import random
import unittest
from unittest.mock import patch

import jeu
import moteur as M
from regles import REGLES


class Lot4Tests(unittest.TestCase):
    def test_saisie_historique(self):
        self.assertEqual(jeu.lire_historique('[0, 0, -1]'), [0, 0, -1])
        for texte in ('{}', '[true]', '[1.5]', '["1"]', '__import__("os")'):
            with self.subTest(texte=texte), self.assertRaises(ValueError):
                jeu.lire_historique(texte)

    def test_rejeu_refus_et_regles_actives(self):
        sortie = io.StringIO()
        # Première liste : retrait adverse interdit. Deuxième : carré gagnant.
        with patch('builtins.input', side_effect=['[0,-1]', '[0,6,1,6,0,5,1]']), contextlib.redirect_stdout(sortie):
            etat = jeu.rejouer_depuis_terminal()
        self.assertIn('Rejeu refusé', sortie.getvalue())
        self.assertEqual(M.gagnant(etat), 'X')
        self.assertEqual(etat, M.rejouer(etat['coups'], REGLES))

    def test_historique_sans_jouer_et_fin_de_partie(self):
        sortie = io.StringIO()
        with patch('builtins.input', side_effect=['h', 'abc', '9', '0', '6', '1', '6', '0', '5', '1']), contextlib.redirect_stdout(sortie):
            etat = jeu.lancer_partie()
        self.assertEqual(etat['coups'], [0, 6, 1, 6, 0, 5, 1])
        self.assertIn('Historique des coups :\n[]', sortie.getvalue())
        self.assertIn(str(etat['coups']), sortie.getvalue())
        self.assertEqual(M.gagnant(etat), 'X')

    def test_trente_parties_ordinateur_reproductibles(self):
        for graine in range(30):
            hasard = random.Random(graine)
            def humain(etat):
                return hasard.choice(M.coups_possibles(etat))
            with patch('jeu.saisir_coup', side_effect=humain), patch('jeu.random.choice', side_effect=hasard.choice), contextlib.redirect_stdout(io.StringIO()):
                etat = jeu.lancer_partie(ordinateur=True)
            self.assertTrue(etat['fini'])
            self.assertLessEqual(len(etat['coups']), 84)
            self.assertEqual(etat, M.rejouer(etat['coups'], REGLES))


if __name__ == '__main__':
    unittest.main()
