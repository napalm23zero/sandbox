import unittest
from itertools import count

from pipeline import first_squares, parse_numbers


class PipelineTest(unittest.TestCase):
    def test_squares_the_numbers_and_skips_the_rest(self):
        self.assertEqual(first_squares(["1", "two", "-3", " 4 "], 3, []), [1, 9, 16])

    def test_reads_only_as_far_as_needed(self):
        log = []
        first_squares(["1", "two", "3", "4", "5"], 2, log)
        self.assertEqual(len(log), 3)

    def test_works_on_an_infinite_source(self):
        endless = (str(n) for n in count(1))
        self.assertEqual(first_squares(endless, 4, []), [1, 4, 9, 16])

    def test_a_generator_is_single_use(self):
        numbers = parse_numbers(["1", "2"])
        self.assertEqual(list(numbers), [1, 2])
        self.assertEqual(list(numbers), [])


if __name__ == "__main__":
    unittest.main()
