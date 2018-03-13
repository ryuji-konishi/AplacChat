import unittest
import Dictionary as dic

class TestAtomicParser(unittest.TestCase):
    def setUp(self):
        pass
        
    def test_English(self):
        eng = dic.Dictionary()
        self.assertTrue(eng.Check("Apple"))
        

if __name__ == "__main__":
    unittest.main()

