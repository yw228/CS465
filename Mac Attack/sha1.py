import struct
import io

def left_rotate(n, b):
    # Function to perform a left rotation on a 32-bit integer
    return ((n << b) | (n >> (32 - b))) & 0xffffffff


def process_data(data, h):
    # Function to process a 64-byte chunk of data using SHA-1 algorithm
    w = [0] * 80

    # Convert the 64-byte chunk into a list of 32-bit integers
    for i in range(16):
        w[i] = struct.unpack(b'>I', data[i * 4:i * 4 + 4])[0]

    # Extend the list of 32-bit integers to 80 using a specific algorithm
    for i in range(16, 80):
        w[i] = left_rotate(w[i - 3] ^ w[i - 8] ^ w[i - 14] ^ w[i - 16], 1)

    a, b, c, d, e = h

    # Main SHA-1 algorithm loop
    for i in range(80):
        if 0 <= i <= 19:
            f = d ^ (b & (c ^ d))
            k = 0x5A827999
        elif 20 <= i <= 39:
            f = b ^ c ^ d
            k = 0x6ED9EBA1
        elif 40 <= i <= 59:
            f = (b & c) | (b & d) | (c & d)
            k = 0x8F1BBCDC
        elif 60 <= i <= 79:
            f = b ^ c ^ d
            k = 0xCA62C1D6

        # SHA-1 operations on a, b, c, d, e
        a, b, c, d, e = (left_rotate(a, 5) + f + e + k + w[i] & 0xffffffff,
                         a, left_rotate(b, 30), c, d)

    # Update hash values based on processed chunk
    return [(h[i] + x) & 0xffffffff for i, x in enumerate([a, b, c, d, e])]


class Sha1Hash:
    def __init__(self):
        # Initialize the SHA-1 hash object with specific initial hash values
        # Given Mac address
        self.h = [0xe384efad, 0xf26767a6, 0x13162142, 0xb5ef0efb, 0xb9d7659a]
        self.unprocessed = b''  # Buffer for unprocessed data
        self.message_byte_length = 128  # Initial message byte length

    def update(self, arg):
        # Method to update the hash object with input data
        if isinstance(arg, (bytes, bytearray)):
            arg = io.BytesIO(arg)

        chunk = self.unprocessed + arg.read(64 - len(self.unprocessed))
        # Process 64-byte chunks until no complete chunks are left
        while len(chunk) == 64:
            self.h = process_data(chunk, self.h)
            self.message_byte_length += 64
            chunk = arg.read(64)

        # Store the remaining unprocessed data
        self.unprocessed = chunk
        return self

    def digest(self):
        # Method to get the binary digest of the hash object
        return b''.join(struct.pack(b'>I', x) for x in self._produce_digest())

    def hexdigest(self):
        # Method to get the hexadecimal digest of the hash object
        return '%08x%08x%08x%08x%08x' % tuple(self._produce_digest())

    def _produce_digest(self):
        # Internal method to produce the final digest of the hash object
        message = self.unprocessed
        message_byte_length = self.message_byte_length + len(message)
        message += b'\x80'  # Padding with '1' bit and '0' bits until length is congruent to 448 (mod 512)
        message += b'\x00' * ((56 - (message_byte_length + 1) % 64) % 64)  # Add '0' bits
        message_bit_length = message_byte_length * 8
        message += struct.pack(b'>Q',
                               message_bit_length)  # Append the original message length as a 64-bit big-endian integer

        # Process message chunks and return the final hash values
        h = process_data(message[:64], self.h)
        if len(message) == 64:
            return h
        return process_data(message[64:], h)


def sha1(data):
    # Function to compute the SHA-1 hash of the input data
    return Sha1Hash().update(data).hexdigest()

