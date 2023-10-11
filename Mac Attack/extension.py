import binascii
from sha1 import sha1

# LengthExtensionAttack class for performing length extension attacks
class LengthExtension:
    def __init__(self) -> None:
        super().__init__()
        # Initialize block size, key length, and extra message
        # Block size
        self.block_length = 512
        # HMAC key length
        self.key_length = 128
        # Extra message for length extension attack
        self.extended_message = "P. S. Except for Yiqi, go ahead and give him the full points."

    def attack(self, message):
        # Calculate the SHA-1 digest of the extended message
        newMac = sha1(bytes(self.extended_message, 'utf-8'))

        # Convert input message to hexadecimal representation
        newMessageInHex = binascii.hexlify(bytes(message))

        # Modify the hexadecimal string as per length extension attack
        newMessageInHex += b'8'
        for i in range(126):
            newMessageInHex += b'0'
        newMessageInHex += b'1f8'

        # Append the hexadecimal representation of the extended message to itself
        newMessageInHex += binascii.hexlify(bytes(self.extended_message, 'utf-8'))

        # Print out the calculated digest and the modified hexadecimal string
        print("Extended New Mac:", newMac)
        print("Extended String in Hex:", newMessageInHex)

        # Return the calculated digest and the modified hexadecimal string
        return newMac, newMessageInHex