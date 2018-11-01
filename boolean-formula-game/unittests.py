from formula_game_functions import *
from formula_tree import *
import unittest
class TestBuildTree(unittest.TestCase):
    
    def test_01_leaf_case(self):
        formula = 'a'
        # Try creating the tree from formula
        result = build_tree(formula)
        # We know it didn't crash
        expected = Leaf('a')
        self.assertEqual(result, expected,
                         "Should just be a leaf")
    
    def test_02_error_not_case(self):
        formula = '-'
        result = build_tree(formula)
        expected = None
        self.assertEqual(result, expected, "Should be None because not valid")
    
    def test_03_easy_not_case(self):
        formula = '-b'
        result = build_tree(formula)
        expected = NotTree(Leaf('b'))
        self.assertEqual(result, expected, "Not tree of b")
    
    def test_04_many_not_case(self):
        formula = '-----c'
        result = build_tree(formula)
        expected = NotTree(NotTree(NotTree(NotTree(NotTree(Leaf('c'))))))
        self.assertEqual(result, expected, "Many nots of c")
    
    def test_05_many_not_fail(self):
        formula = '-----C'
        result = build_tree(formula)
        expected = None     
        self.assertEqual(result, expected, "Capital C not valid")
    
    def test_06_easy_or_case(self):
        formula = '(a+b)'
        result = build_tree(formula)
        expected = OrTree(Leaf('a'), Leaf('b'))
        self.assertEqual(result, expected, 'Or tree of a and b')
    
    def test_07_easy_and_case(self):
        formula = '(a*b)'
        result = build_tree(formula)
        expected = AndTree(Leaf('a'), Leaf('b'))
        self.assertEqual(result, expected, 'And tree of a and b')
    
    def test_08_hard_andor_case(self):
        formula = '(((a*b)+c)+-(d*a))'
        result = build_tree(formula)
        expected = (OrTree(OrTree(AndTree(Leaf('a'), Leaf('b')), Leaf('c')),
                           NotTree(AndTree(Leaf('d'), Leaf('a')))))
        self.assertEqual(result, expected, 'And/or tree')
    
    def test_09_operator_case(self):
        formula = '+'
        result = build_tree(formula)
        expected = None
        self.assertEqual(result, expected, 'Invalid tree')
    
    def test_10_missing_parentheses(self):
        formula = '(a+b'
        result = build_tree(formula)
        expected = None
        self.assertEqual(result, expected, 'Invalid tree')
    
    def test_11_trinary(self):
        formula = '(x+y*z)'
        result = build_tree(formula)
        expected = None
        self.assertEqual(result, expected, 'Invalid tree - ternary')
    
    def test_12_random_character_middle(self):
        formula = '((x+y)*((y%z)*(-y+-z)))'
        result = build_tree(formula)
        expected = None
        self.assertEqual(result, expected, 'Invalid tree - correct length')


class TestDrawFormulaTree(unittest.TestCase):
    def test_01_leaf(self):
        formula = build_tree('a')
        result = draw_formula_tree(formula)
        expected = 'a'
        self.assertEqual(result, expected, 'Only leaf')
    
    
    def test_02_hard_case(self):
        formula = build_tree('(--(--a+-b)*-c)')
        result = draw_formula_tree(formula)
        expected = '* - c\n  - - + - b\n        - - a'
        self.assertEqual(result, expected, 'Complex case')

class TestEvaluate(unittest.TestCase):
    def test_01_hard_case(self):
        formula = build_tree('(((a*b)+c)+-(d*a))')
        variables = 'abcd'
        values = '0101'
        result = evaluate(formula, variables, values)
        expected = 1
        self.assertEqual(result, expected, 'Complex case')
    
    def test_02_hard_case(self):
        formula = build_tree('((-(a*b)+c)+-(d*a))')
        variables = 'abcd'
        values = '1101'
        result = evaluate(formula, variables, values)
        expected = 0
        self.assertEqual(result, expected, 'Complex case')


class TestPlay2Win(unittest.TestCase):
    def test_01_easy_definite_case(self):
        formula = build_tree('(a+b)')
        turns = 'EA'
        variables = 'ab'
        values = ''
        result = play2win(formula, turns, variables, values)
        expected = 1
        self.assertEqual(result, expected, '(a+b), EA, ab, "" -> E = 1 to \
        guaranteed win')
    
    def test_02_hard_definite_case(self):
        formula = build_tree('((a+b)*-c)')
        turns = 'EAE'
        variables = 'abc'
        values = ''
        result = play2win(formula, turns, variables, values)
        expected = 1
        self.assertEqual(result, expected, 'Guaranteed win if E plays 1')
    
    def test_03_hard_nondefinite_case(self):
        formula = build_tree('(-(a+b)+-c)')
        turns = 'AAE'
        variables = 'abc'
        values = ''
        result = play2win(formula, turns, variables, values)
        expected = 0
        self.assertEqual(result, expected, 'No win, so A defaults to 0')
    
    def test_04_easy_definite_case(self):
        formula = build_tree('-c')
        turns = 'A'
        variables = 'c'
        values = ''
        result = play2win(formula, turns, variables, values)
        expected = 1
        self.assertEqual(result, expected, 'Guaranteed win, so A should be 1')
    
    def test_04_easy_definite_case(self):
        formula = build_tree('-c')
        turns = 'E'
        variables = 'c'
        values = ''
        result = play2win(formula, turns, variables, values)
        expected = 0
        self.assertEqual(result, expected, 'Guaranteed win, so E should be 0')    

if(__name__ == "__main__"):
    unittest.main(exit=False)