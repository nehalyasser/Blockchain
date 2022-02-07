import hashlib
import string
import time
import random


class Ledger:
    
    def __init__(self, index, transactions, timestamp, prevHash):

        self.index = index 
        self.transactions = transactions 
        self.timestamp = timestamp
        self.proof = self.get_proof_work()
        self.prevHash = prevHash
        self.blockTotalData = self.index + " - ".join(self.transactions) + " - " + self.timestamp + " - " 
        + self.proof + " - " + self.prevHash + " - " + self.proof    
        #blockString= self.index + self.transactions + self.timestamp+ self.proof + self.precHash + self.proof    
        self.hash = hashlib.sha256(self.blockTotalData .encode()).hexdigest()
        
    def get_proof_work (self):
        
        proofFound= False
        while proofFound == False:
            proof= ''.join(random.choice(string.digits)for x in range(64))
            #block= self.index + self.transactions + self.timestamp+ self.proof + self.precHash + self.proof    
            block = self.index + " - ".join(self.transactions) + " - " + self.timestamp + " - " 
            + self.proof + " - " + self.prevHash + " - " + self.proof    
            blockHash=hashlib.sha256(block.encode()).hexdigest()
            if blockHash.startswith('000'):
                print (blockHash)
                proofFound=True
                
        return proof

class BlockChain:

    def __init__(self):
        
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        
        genesis_block = Ledger(0, [], time.time(), "0")
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)






