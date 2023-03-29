class Codec:
    H = [
        [0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0],
        [1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
        [1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        [0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0],
        [1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1]
    ]

    H_ROWS = len(H)
    H_COLS = len(H[0])

    @staticmethod
    def encode(message):
        """
        Encodes a message into a form that allows correction of up to two bit errors during decoding

        :param message: An array of bits to be encoded
        :return: An encoded message in the form of a bit array that is twice the size of the input array
        """
        padded = Codec.add_padding(message)
        blocks = Codec.split_into_blocks(padded)
        encoded = []
        for block in blocks:
            block.extend([0 for _ in range(0, Codec.H_ROWS)])

            # Calculate parity bits
            for parity_index in range(0, Codec.H_ROWS):
                for h_index in range(0, Codec.H_ROWS):
                    block[parity_index + 8] += Codec.H[parity_index][h_index] * block[h_index]
                block[parity_index + 8] %= 2

            encoded.extend(block)
        return encoded

    @staticmethod
    def decode(message):
        """
        Decodes a previously decoded message correcting all bit errors or raises an exception if the input size is not
        a multiple of word size

        :param message: A previously encoded message in the form of array of bits
        :return: A decoded message in the form of bit array
        """
        if len(message) % Codec.H_COLS != 0:
            raise Exception('Failed to decode the message: Invalid length')

        blocks = Codec.split_into_double_blocks(message)
        decoded = []
        for i in range(0, len(blocks)):
            decoded.extend(Codec.decode_word(blocks[i]))

        return decoded

    @staticmethod
    def decode_word(word):
        """
        Decodes a single word of two bytes in size or raises an exception if the parameter has invalid size

        :param word: A word to be decoded in the form of array of bits
        :return: A decoded word of one byte in size in the form of array of bits
        """
        if len(word) != Codec.H_COLS:
            raise Exception('Failed to decode the word: Invalid length')

        word = word.copy()
        errors = Codec.get_errors(word)

        # Correct single error
        for col in range(0, Codec.H_COLS):
            for row in range(0, Codec.H_ROWS):
                if errors[row] != Codec.H[row][col]:
                    break
            else:
                word[col] ^= 1

        # Correct double error
        for i in range(0, Codec.H_COLS):
            for j in range(1, Codec.H_COLS):
                for row in range(0, Codec.H_ROWS):
                    if (Codec.H[row][i] ^ Codec.H[row][j]) != errors[row]:
                        break
                else:
                    word[i] ^= 1
                    word[j] ^= 1
                    return word[0:8]

        return word[0:8]

    @staticmethod
    def add_padding(message):
        """
        Pads the input array with zeros to a multiple of a byte size

        :param message: An array of bits to be extended
        :return: A padded message
        """
        ret = [v for v in message]
        if len(ret) % 8 != 0:
            ret.extend([0 for _ in range(0, (8 - len(ret) % 8))])
        return ret

    @staticmethod
    def split_into_blocks(message):
        """
        Splits the message into one-byte blocks or raises an exception if the input array size is not multiple of byte

        :param message: An array of bits to be split
        :return: An array of one-byte blocks where each block is an array of eight bits
        """
        if len(message) % 8 != 0:
            raise Exception('Failed to split the message into blocks: Invalid length')
        return [message[i:i+8] for i in range(0, len(message), 8)]

    @staticmethod
    def split_into_double_blocks(message):
        """
        Splits the message into two-byte blocks or raises an exception if the input array size is not multiple of two
        bytes

        :param message: An array of bits to be split
        :return: An array of double-byte blocks where each block is an array of sixteen bits
        """
        if len(message) % 16 != 0:
            raise Exception('Failed to split the message into double blocks: Invalid length')
        return [message[i:i+16] for i in range(0, len(message), 16)]

    @staticmethod
    def get_errors(message):
        """
        Returns a list of errors

        :param message: A previously encoded message to be checked for errors
        :return: A list of errors
        """
        if len(message) % Codec.H_COLS != 0:
            raise Exception('Failed to get errors: Invalid length')
        errors = []
        for row in range(0, Codec.H_ROWS):
            e = 0
            for col in range(0, Codec.H_COLS):
                e += Codec.H[row][col] * message[col]
            errors.append(e % 2)
        return errors
