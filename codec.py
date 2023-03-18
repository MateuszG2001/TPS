class Codec:
    H = [
        [1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0],
        [1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0],
        [1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0],
        [1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1]
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
        errors = Codec.get_errors(message)
        decoded = [(message[i] + errors[i]) % 2 for i in range(0, Codec.H_ROWS)]
        return decoded

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
        found = False
        for row in range(0, Codec.H_ROWS):
            e = 0
            for col in range(0, Codec.H_COLS):
                e += Codec.H[row][col] * message[col]
                e %= 2
            if e == 1:
                found = True
            errors.append(e)

        if found:
            errors = [b ^ 1 for b in errors]

        errors.reverse()
        return errors
