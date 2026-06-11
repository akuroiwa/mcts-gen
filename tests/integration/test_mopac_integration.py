import unittest
import re
from mcts_gen.services.mopac_evaluator import MopacEvaluator

class TestMopacIntegration(unittest.TestCase):
    def test_output_parsing(self):
        sample_output = "FINAL HEAT OF FORMATION =         -123.45678 KCAL/MOL"
        match = re.search(r"FINAL HEAT OF FORMATION\s+=\s+(-?\d+\.\d+)\s+KCAL/MOL", sample_output)
        self.assertIsNotNone(match)
        self.assertEqual(float(match.group(1)), -123.45678)

if __name__ == "__main__":
    unittest.main()
