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

    @staticmethod
    def encode(message):
        padded = Codec.add_padding(message)
        padded.extend([0 for _ in range(0, len(padded))])
        return padded

    @staticmethod
    def decode(message):
        if len(message) % 16 != 0:
            raise Exception('Failed to decode the message: Invalid length')
        decoded = [message[i] for i in range(0, len(message) // 2)]
        return decoded

    @staticmethod
    def add_padding(message):
        ret = [v for v in message]
        if len(ret) % 8 != 0:
            ret.extend([0 for _ in range(0, (8 - len(ret) % 8))])
        return ret
