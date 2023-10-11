import hashlib
import string
import random


def generateRandomString():
    numChar = random.randrange(1, 32)
    text = ''
    for i in range(numChar):
        text = text + random.choice(string.printable)
    # print("Random text is " + text)
    return text


class Hash:
    def __init__(self, inputString, size):
        self.string = inputString
        self.size = size
        self.mask = 0
        for i in range(size):
            self.mask = (self.mask << 1) + 1
    def truncateDigest(self, digest):
        digest = int(digest, 16)
        digest = digest & self.mask
        digest = format(digest, 'x')
        return digest

    def startAttacks(self):
        self.collisionAttack()
        self.preImageAttack()

    def collisionAttack(self):
        print('starting collision attack')
        print('=========================================================')
        totalCount = 0
        for i in range(100):
            hashes = {}
            count = 0
            while True:
                count = count + 1
                text = generateRandomString()
                # print('Input = ' + str(self.string))
                digest = hashlib.sha1(text.encode()).hexdigest()
                # print('Digest = ' + digest)
                digest = self.truncateDigest(digest)
                # print('truncated digest = ' + digest)
                if (digest in hashes) and (hashes[digest] != text):
                    break
                hashes[digest] = text
            totalCount += count
        print("Total Counts for 100 times are: " + str(totalCount))
        print('Average is :' + str(totalCount / 100))

    def preImageAttack(self):
        print('Starting pre-image attack')
        print('=========================================================')
        digest = hashlib.sha1(self.string.encode()).hexdigest()
        # print('input = ' + str(self.string))
        # print('Digest = ' + str(digest))
        digest = self.truncateDigest(digest)
        # print('truncated digest = ' + str(digest))
        totalCount = 0
        for i in range(100):
            count = 0
            # print(i + "Loop")
            while True:
                count = count + 1
                text = generateRandomString()
                newDigest = hashlib.sha1(text.encode()).hexdigest()
                newDigest = self.truncateDigest(newDigest)
                if digest == newDigest:
                    break
            totalCount += count
        print("Total Counts for 100 times are:  " + str(totalCount))
        print('Average is : ' + str(totalCount / 100))

