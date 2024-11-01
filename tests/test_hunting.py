import os
import unittest
from data_hunter.main import MovieDataHunter


class TestMovieDataHunter(unittest.TestCase):

    def setUp(self):
        self.data_hunter = MovieDataHunter(categories=["Bollywood"], genre=["Action"])

    def test_hunt(self):
        resp = self.data_hunter.hunt(limit=20)
        self.assertIsInstance(resp["movies_count"], int)
        self.assertIsInstance(resp["genres"], list)
        saved_to = resp["saved_to"][0]
        self.assertTrue(saved_to.is_file())
        os.remove(saved_to)


if __name__ == "__main__":
    unittest.main()
