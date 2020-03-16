import unittest
import producer
from decimal import Decimal


class TestJsonProducer(unittest.TestCase):
    def setUp(self):
        self.message = producer.MatchPrice()
        self.match_i_range = 100000
        self.price_i_range = 10000

    def test_rand_match_type(self):
        self.assertTrue(type(self.message.rand_match()) == int)

    def test_rand_match_lower_bound(self):
        for i in range(self.match_i_range):
            message = producer.MatchPrice()
            self.assertLess(99, message.rand_match())

    def test_rand_match_upper_bound(self):
        for i in range(self.match_i_range):
            message = producer.MatchPrice()
            self.assertGreater(1000, message.rand_match())

    def test_rand_price_type(self):
        message = producer.MatchPrice()
        self.assertTrue(type(message.rand_price()) == Decimal)

    def test_rand_price_lower_bound(self):
        for i in range(self.price_i_range):
            message = producer.MatchPrice()
            self.assertLess(0.99, message.rand_price())

    def test_rand_price_upper_bound(self):
        for i in range(self.price_i_range):
            message = producer.MatchPrice()
            self.assertGreater(10.01, message.rand_price())

    def test_message_format(self):
        message = producer.MatchPrice(match=100, price=9.09)
        print(message.format_message())
        self.assertTrue(message.format_message() == '{"match": 100, "price": 9.09}')


if __name__ == '__main__':
    unittest.main()
