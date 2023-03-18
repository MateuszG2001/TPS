import unittest
from codec import *


class CodecTest(unittest.TestCase):
    def test_add_padding_if_message_of_length_equal_to_byte_then_returns_non_modified_message(self):
        message = [0, 1, 1, 0, 1, 0, 1, 0]
        self.assertEqual(message, Codec.add_padding(message))

    def test_add_padding_if_message_of_length_equal_to_byte_then_the_returned_message_is_a_copy(self):
        message = [0, 0, 0, 0, 0, 0, 0, 0]
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

    def test_encode_if_message_of_length_equal_to_byte_then_returns_message_twice_as_long(self):
        message = [0, 1, 1, 0, 0, 0, 1, 1]
        self.assertEqual(16, len(Codec.encode(message)))

    def test_encode_if_message_of_length_less_than_byte_then_extends_to_appropriate_size(self):
        message = [0, 0, 1]
        self.assertEqual(16, len(Codec.encode(message)))

    def test_encode_if_message_length_is_multiple_of_byte_then_returns_message_twice_as_long(self):
        message = [0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0]
        self.assertEqual(32, len(Codec.encode(message)))

    def test_encode_if_message_length_is_not_multiple_of_byte_then_extends_to_appropriate_size(self):
        message = [0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1]
        self.assertEqual(32, len(Codec.encode(message)))

    def test_decode_if_message_length_less_than_two_bytes_then_raises_exception(self):
        message = [0, 1, 1, 0, 1]
        self.assertRaises(Exception, lambda: Codec.decode(message))

    def test_decode_if_message_length_equal_to_two_bytes_then_returns_message_twice_as_short(self):
        message = [0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0]
        self.assertEqual(8, len(Codec.decode(message)))

    def test_decode_if_message_length_is_multiple_of_two_bytes_then_returns_message_twice_as_short(self):
        message = [0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0]
        self.assertEqual(16, len(Codec.decode(message)))


if __name__ == '__main__':
    unittest.main()
