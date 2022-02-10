import hashlib
from operator import truediv
import string
import time
import random

i = 5
Zeros = 2
transaction_list = ["Anna Sends Mike 100", "Mike sends Bob 200 LE",
                    "Bob sends Micheal 50 LE", "Anna sends Micheal 170 LE",
                    "Bob sends Anna 60 LE", "Micheal sends Anna 100 LE",
                    "Micheal sends Mike 150 LE", "Mike sends Anna 60 LE",
                    "Mike sends Micheal 100 LE", "Mahsun sends Mike 80 LE",
                    "Anne sends Mahsun 150 LE", "Micheal Sends Mahsun 200 LE"]
prev_hash_main = ""
prev_hash_attacker = ""
prev_hash_others = ""
attacker_index = ""
others_index = ""
attacker_precentage = 600


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
                # print(blockHash)
                proofFound = True
            if proofFound is True:
                # print(proof)
                # print(self.index)
                return proof
        return -1

    def compute_hash(self):
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

    def get_unconfirmed_transaction(self):
        t = self.unconfirmed_transactions
        self.unconfirmed_transactions = []
        return t

    def is_valid_hash(self, block, block_hash):
        return (block_hash.startswith('0' * Zeros) and
                block_hash == block.compute_hash())

    # Function that add block to a chain
    def add_block(self, block, hash):
        """
        * Checking if the proof is valid.
        * The previous_hash referred in the block and the hash of latest block
          in the chain match.
        """
        previous_hash = (self.prev_hash())
        print("add_block")
        # print(previous_hash)
        # print(block.prevHash)
        if previous_hash != block.prevHash:
            self.unconfirmed_transactions = []
            return False, block.transactions

        if not self.is_valid_hash(block, hash):
            return False

        #block.hash = hash
        self.chain.append(block)
        return True

    def mining(self, prev_hash):
        if not len(self.unconfirmed_transactions):
            return False

        transaction = check_transaction(self.unconfirmed_transactions)
        last = self.print_previous_block()
        last_hash = prev_hash
        timee = time.time()
        index = int(last.index) + 1
        new_block = Ledger(str(index), transaction,
                           str(timee), last_hash)
        hash = new_block.block_hash
        x = self.add_block(new_block, hash)
        print(x)
        if x:
            self.unconfirmed_transactions = []
            return new_block.index, True
        else:
            return new_block, False


class Chainn:
    def __init__(self, index):
        self.chain = []
        self.index = int(index)
    # This function is created
    # to display the previous block

    def print_previous_block(self):
        return self.chain[-1]

    def prev_hash(self):
        return ((self.print_previous_block()).block_hash)

    def is_valid_hash(self, block, block_hash):
        return (block_hash.startswith('0' * Zeros) and
                block_hash == block.compute_hash())

    # Function that add block to a chain
    def add_block(self, block, hash):
        """
        * Checking if the proof is valid.
        * The previous_hash referred in the block and the hash of latest block
          in the chain match.
        """
        if len(self.chain) > 0:
            previous_hash = block.prevHash
            print("add_block")
            print(previous_hash)
            print(block.prevHash)
            if previous_hash != block.prevHash:
                return False

            if not self.is_valid_hash(block, hash):
                return False

            self.chain.append(block)
            return True
        else:
            self.chain.append(block)
            return True

    def mining(self, transaction, prev_hash):
        if len(self.chain) == 0:
            index = self.index
            print(index)
            transactionn = check_transaction(transaction)
            timee = time.time()
            new_block = Ledger(str(index), transactionn,
                               str(timee), prev_hash)
            hash = new_block.block_hash
            x = self.add_block(new_block, hash)
            print(x)
        else:
            last = self.print_previous_block()
            last_hash = prev_hash
            timee = time.time()
            transactionn = check_transaction(transaction)
            index = int(last.index) + 1
            new_block = Ledger(str(index), transactionn,
                               str(timee), last_hash)
            hash = new_block.block_hash
            x = self.add_block(new_block, hash)
            print(x)
        if x:
            self.unconfirmed_transactions = []
            return new_block.index, True
        else:
            return new_block, False

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


# First for loop to generate the main Block:
main_chain = BlockChain()

for x in range(4):
    t1 = generation()
    main_chain.add_new_transaction(t1)
    t2 = generation()
    main_chain.add_new_transaction(t2)
    t3 = generation()
    main_chain.add_new_transaction(t3)
    prev_hash_main = main_chain.prev_hash()
    main_chain.mining(prev_hash_main)
    print(x)

for x in main_chain.chain:
    print(x.__dict__)
    # print(x.block_hash)

prev_hash_attacker = prev_hash_main
prev_hash_others = main_chain.prev_hash()
attacker_index = len(main_chain.chain) - 1
other_index = len(main_chain.chain)
c1 = Chainn(attacker_index)
c2 = Chainn(other_index)

for x in range(5):
    for y in range(i):
        x = random.randint(0, 1000)
        t1 = generation()
        main_chain.add_new_transaction(t1)
        t2 = generation()
        main_chain.add_new_transaction(t2)
        t3 = generation()
        main_chain.add_new_transaction(t3)
        if x < attacker_precentage:
            transaction = main_chain.get_unconfirmed_transaction()
            c1.mining(transaction, prev_hash_attacker)
            prev_hash_attacker = c1.prev_hash()
        else:
            transaction = main_chain.get_unconfirmed_transaction()
            c2.mining(transaction, prev_hash_others)
            prev_hash_others = c2.prev_hash()


print("Printing of C1")
for x in c1.chain:
    print(x.__dict__)
    # print(x.block_hash)

print("Printing of C2")
for x in c2.chain:
    print(x.__dict__)
    # print(x.block_hash)
