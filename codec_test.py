import unittest
from itertools import product, combinations
from scipy.spatial.distance import hamming
from random import randint

from codec import *


class CodecTest(unittest.TestCase):
    def test_add_padding_if_message_of_length_equal_to_byte_then_returns_non_modified_message(self):
        message = [0, 1, 1, 0, 1, 0, 1, 0]
        self.assertEqual(message, Codec.add_padding(message))

    def test_add_padding_if_message_of_length_equal_to_byte_then_the_returned_message_is_a_copy(self):
        message = [0 for _ in range(0, 8)]
        ret = Codec.add_padding(message)
        message[0] = message[2] = 1
        self.assertNotEqual(ret, message)

    def test_add_padding_if_message_of_length_less_than_one_byte_then_extends_to_appropriate_size(self):
        message = [1, 0, 1]
        self.assertEqual(8, len(Codec.add_padding(message)))

    def test_add_padding_if_message_length_is_multiple_of_byte_then_returns_non_modified_message(self):
        message = [0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0]
        self.assertEqual(message, Codec.add_padding(message))

    def test_add_padding_if_message_length_is_not_multiple_of_byte_then_extends_to_appropriate_size(self):
        message = [0, 1, 0, 1, 0, 0, 1, 0, 1, 0]
        self.assertEqual(16, len(Codec.add_padding(message)))

    def test_encode_if_message_of_length_equal_to_byte_then_returns_message_of_appropriate_length(self):
        message = [0 for _ in range(0, 8)]
        self.assertEqual(Codec.H_COLS, len(Codec.encode(message)))

    def test_encode_if_message_of_length_less_than_byte_then_extends_to_appropriate_size(self):
        message = [0, 0, 1]
        self.assertEqual(Codec.H_COLS, len(Codec.encode(message)))

    def test_encode_if_message_length_is_multiple_of_byte_then_returns_message_of_appropriate_length(self):
        message = [randint(0, 1) for _ in range(0, 2*8)]
        self.assertEqual(2*Codec.H_COLS, len(Codec.encode(message)))

    def test_encode_if_message_length_is_not_multiple_of_byte_then_extends_to_appropriate_size(self):
        message = [randint(0, 1) for _ in range(0, 2*8 - 1)]
        self.assertEqual(2*Codec.H_COLS, len(Codec.encode(message)))

    def test_encode_if_valid_input_then_returned_message_consists_only_of_ones_and_zeroes(self):
        message = [0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0]
        self.assertEqual({0, 1}, set(Codec.encode(message)))

    def test_encode_if_every_byte_combination_provided_then_encoded_bytes_are_unique(self):
        encoded_list = list()
        for c in product([0, 1], repeat=8):
            encoded = Codec.encode(c)
            self.assertTrue(encoded not in encoded_list)
            encoded_list += [encoded]

    @unittest.skip
    def test_encode_if_every_byte_combination_provided_then_the_minimum_hamming_distance_is_five(self):
        encoded_list = list()
        for c in product([0, 1], repeat=8):
            encoded = Codec.encode(c)
            for el in encoded_list:
                self.assertGreaterEqual(hamming(encoded, el) * len(encoded), 5)
            encoded_list += [encoded]

    def test_decode_if_message_length_less_than_two_bytes_then_raises_exception(self):
        message = [0, 1, 1, 0, 1]
        self.assertRaises(Exception, lambda: Codec.decode(message))

    def test_decode_if_message_length_equal_to_h_cols_then_returns_message_of_length_equal_to_one_byte(self):
        message = [randint(0, 1) for _ in range(0, Codec.H_COLS)]
        self.assertEqual(8, len(Codec.decode(message)))

    def test_decode_if_message_length_is_multiple_of_h_cols_then_returns_message_of_appropriate_length(self):
        message = [randint(0, 1) for _ in range(0, 2*Codec.H_COLS)]
        self.assertEqual(8, len(Codec.decode(message)))

    def test_split_into_blocks_if_message_length_is_not_multiple_of_byte_then_raises_exception(self):
        message = [1, 0, 1]
        self.assertRaises(Exception, lambda: Codec.split_into_blocks(message))

    def test_split_into_blocks_if_message_length_is_multiple_of_byte_then_splits_into_blocks(self):
        message = [
            1, 0, 1, 0, 1, 1, 0, 1,
            0, 0, 1, 1, 0, 0, 0, 1,
            0, 1, 1, 1, 1, 1, 0, 0,
            0, 0, 0, 1, 0, 0, 1, 0
        ]
        self.assertEqual(4, len(Codec.split_into_blocks(message)))

    def test_get_errors_if_message_length_is_not_multiple_of_two_bytes_then_raises_exception(self):
        message = [1, 0, 1]
        self.assertRaises(Exception, lambda: Codec.get_errors(message))

    def test_get_errors_if_no_errors_then_returns_a_list_of_only_zeros(self):
        encoded = Codec.encode([0, 0, 1, 1, 0, 0, 0, 1])
        self.assertEqual([0 for _ in range(0, Codec.H_ROWS)], Codec.get_errors(encoded))

    def test_get_errors_if_single_error_then_returns_list_with_one_at_the_position_at_which_error_occurred(self):
        encoded = Codec.encode([randint(0, 1) for _ in range(0, 8)])
        pos = randint(0, Codec.H_ROWS - 1)
        encoded[pos] ^= 1
        expected = [0 for _ in range(0, Codec.H_ROWS)]
        expected[pos] = 1
        self.assertEqual(expected, Codec.get_errors(encoded))

    def test_decode_if_single_error_then_it_is_corrected(self):
        for message in product([0, 1], repeat=8):
            encoded = Codec.encode(message)
            for i in range(0, Codec.H_ROWS):
                damaged = encoded.copy()
                damaged[i] ^= 1
                decoded = Codec.decode(damaged)
                self.assertEqual([*message], decoded)

    @unittest.skip
    def test_decode_if_two_errors_then_they_are_corrected(self):
        for message in product([0, 1], repeat=8):
            encoded = Codec.encode(message)
            for i1, i2 in combinations([i for i in range(0, Codec.H_ROWS)], 2):
                damaged = encoded.copy()
                damaged[i1] ^= 1
                damaged[i2] ^= 1
                decoded = Codec.decode(damaged)
                self.assertEqual([*message], decoded)


if __name__ == '__main__':
    unittest.main()
