import unittest
from experimento import CASES,direta,via_skill

class ComparativeLabTests(unittest.TestCase):
    def test_expected_status_in_both_arms(self):
        for name,p,expected in CASES:
            with self.subTest(case=name):
                self.assertEqual(direta(p)['status'],expected)
                self.assertEqual(via_skill(p)['status'],expected)
    def test_identical_implementations(self):
        for _,p,_ in CASES:self.assertEqual(direta(p),via_skill(p))
    def test_repeated_execution(self):
        for _,p,_ in CASES:self.assertEqual(via_skill(p),via_skill(p))

if __name__=='__main__':unittest.main()
