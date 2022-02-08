import hashlib
import string
import time
import random

i = 0
Zeros = 4
transaction_list = ["Anna Sends Mike 100", "Mike sends Bob 200 LE",
                    "Bob sends Micheal 50 LE", "Anna sends Micheal 170 LE",
                    "Bob sends Anna 60 LE", "Micheal sends Anna 100 LE",
                    "Micheal sends Mike 150 LE", "Mike sends Anna 60 LE",
                    "Mike sends Micheal 100 LE"]


class Ledger:

    def __init__(self, index, transactions, timestamp, prevHash):

        self.index = str(index)
        self.transactions = transactions
        self.timestamp = timestamp
        self.prevHash = prevHash
        self.proof = self.calculate_proof_work()
        self.blockTotalData = self.index + \
            " - " + self.transactions + " - " + self.timestamp + \
            " - " + self.prevHash + " - " + self.proof
        # blockString= self.index + self.transactions + self.timestamp+ self.proof + self.precHash + self.proof
        # print(self.blockTotalData)
        self.block_hash = self.compute_hash()
        # print(block_hash)

    def calculate_proof_work(self):

        proofFound = False
        while proofFound == False:
            proof = ''.join(random.choice(string.digits) for x in range(64))
            # block= self.index + self.transactions + self.timestamp+ self.proof + self.precHash + self.proof
            # print(proof)
            block = str(self.index) + " - " + self.transactions + " - " + \
                str(self.timestamp) + " - " + \
                self.prevHash + " - " + str(proof)
            blockHash = hashlib.sha256(block.encode()).hexdigest()
            if blockHash.startswith('0' * Zeros):
                print(blockHash)
                proofFound = True
            if proofFound is True:
                print(proof)
                print(self.index)
                return proof
        return -1

    def compute_hash(self):
        # print(hashlib.sha256(self.blockTotalData.encode()).hexdigest())
        return hashlib.sha256(self.blockTotalData.encode()).hexdigest()

    def get_hash(self):
        return self.block_hash


class BlockChain:

    def __init__(self):
        self.unconfirmed_transactions = []
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):

        timee = time.time()
        genesis_block = Ledger("0", "", str(timee), "0")
        #genesis_block_hash = genesis_block.compute_hash
        # print("aaa")
        # print(genesis_block.block_hash)
        # print(genesis_block.blockTotalData)
        # print("zz")
        self.chain.append(genesis_block)

    # This function is created
    # to display the previous block

    def print_previous_block(self):
        return self.chain[-1]

    def prev_hash(self):
        return ((self.print_previous_block()).block_hash)

    def add_new_transaction(self, transaction):
        # print(len(self.unconfirmed_transactions))
        # print(transaction)
        self.unconfirmed_transactions.append(transaction)

    def is_valid_hash(self, block, block_hash):
        return (block_hash.startswith('0' * Zeros) and
                block_hash == block.compute_hash())

    # Function that add block to a chain
    def add_block(self, block, hash):
        """
        A function that adds the block to the chain after verification.
        Verification includes:
        * Checking if the proof is valid.
        * The previous_hash referred in the block and the hash of latest block
          in the chain match.
        """
        previous_hash = (self.prev_hash())
        print("add_block")
        print(previous_hash)
        print(block.prevHash)
        if previous_hash != block.prevHash:
            return False

        if not self.is_valid_hash(block, hash):
            return False

        #block.hash = hash
        self.chain.append(block)
        return True

    def mining(self):
        if not len(self.unconfirmed_transactions):
            return False

        # print("xx")
        transaction = check_transaction(self.unconfirmed_transactions)
        # print(transaction)
        last = self.print_previous_block()
        last_hash = self.prev_hash()
        timee = time.time()
        index = int(last.index) + 1
        new_block = Ledger(str(index), transaction,
                           str(timee), last_hash)
        #proof = new_block.proof
        hash = new_block.block_hash
        # print(hash)
        x = self.add_block(new_block, hash)
        print(x)
        self.unconfirmed_transactions = []
        return new_block.index
# function to generate random transactions


def generation():
    transaction = ''.join(random.choice(transaction_list))
    return transaction


def check_transaction(transaction):
    if len(transaction) > 1:
        concat_tr = ''
        for x in range(len(transaction)):
            concat_tr += transaction[x]
            if x != (len(transaction)-1):
                concat_tr += "-"
    transaction = concat_tr
    return concat_tr


"""

transaction = [t1, t2]
transaction = check_transaction(transaction)
timex = time.time()
first_block = Ledger("1", transaction, str(timex), "AAA")
print(first_block.blockTotalData)
print(first_block.block_hash)

"""
chainn = BlockChain()
t1 = generation()
# print(t1)
chainn.add_new_transaction(t1)
t2 = generation()
# print(t2)
chainn.add_new_transaction(t2)
t3 = generation()
# print(t3)
chainn.add_new_transaction(t3)
index = chainn.mining()
print(index)

t1 = generation()
chainn.add_new_transaction(t1)
t2 = generation()
chainn.add_new_transaction(t2)
t3 = generation()
chainn.add_new_transaction(t3)
index = chainn.mining()
print(index)

for x in chainn.chain:
    print(x.__dict__)
    # print(x.block_hash)

"""
chainn = chainn.print_previous_block()
x = chainn.index
print(chainn)
print(x)

"""
