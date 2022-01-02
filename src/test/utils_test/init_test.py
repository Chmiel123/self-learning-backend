import unittest

from src.utils import parse_id_range, IdRangeInvalidException


class InitTest(unittest.TestCase):
    def test_parse_id_range(self):
        self.assertEqual((1, 100), parse_id_range('1-100'))
        self.assertEqual((0, 10), parse_id_range('0-10'))
        self.assertEqual((1, 100), parse_id_range('1-100-1000'))
        self.assertRaises(IdRangeInvalidException, parse_id_range, '-1-100')
        self.assertRaises(IdRangeInvalidException, parse_id_range, '1000')
        self.assertRaises(IdRangeInvalidException, parse_id_range, 'asdf')
