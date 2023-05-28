"""File for example test case"""
import unittest
from src.config.test import TEST_USER_ID

class TestExample(unittest.TestCase):
    """Example Test Case"""
    @unittest.skip("Example Test Case")
    def test_example_case(self):
        print(TEST_USER_ID)
        