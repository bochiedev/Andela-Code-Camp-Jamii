import unittest
from .app import addNumber

class TestAddNumbers(unittest.TestCase):
    def test_add_num(self):
        self.assertEqual(addNumber(2, 5), 7)


if __name__ == "__main__":
    unittest.main()
