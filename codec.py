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
        if len(message) % Codec.H_COLS != 0:
            raise Exception('Failed to decode the message: Invalid length')

        message = message.copy()
        errors = Codec.get_errors(message)

        # Correct single error
        for col in range(0, Codec.H_COLS):
            for row in range(0, Codec.H_ROWS):
                if errors[row] != Codec.H[row][col]:
                    break
            else:
                message[col] ^= 1

        # Correct double error
        for i in range(0, Codec.H_COLS):
            for j in range(1, Codec.H_COLS):
                for row in range(0, Codec.H_ROWS):
                    if (Codec.H[row][i] ^ Codec.H[row][j]) != errors[row]:
                        break
                else:
                    message[i] ^= 1
                    message[j] ^= 1
                    return message[0:8]

        return message[0:8]

    @staticmethod
    def add_padding(message):
        ret = [v for v in message]
        if len(ret) % 8 != 0:
            ret.extend([0 for _ in range(0, (8 - len(ret) % 8))])
        return ret

    @staticmethod
    def split_into_blocks(message):
        if len(message) % 8 != 0:
            raise Exception('Failed to split the message into blocks: Invalid length')
        return [message[i:i+8] for i in range(0, len(message), 8)]

    @staticmethod
    def get_errors(message):
        if len(message) % Codec.H_COLS != 0:
            raise Exception('Failed to get errors: Invalid length')
        errors = []
        for row in range(0, Codec.H_ROWS):
            e = 0
            for col in range(0, Codec.H_COLS):
                e += Codec.H[row][col] * message[col]
            errors.append(e % 2)
        return errors
