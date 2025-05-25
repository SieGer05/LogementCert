import time
import json
from .block import Block
from .consensus import ProofOfAuthority

class LogementBlockchain:
   """
   A class to represent a blockchain for managing logement (housing) transactions.
   This blockchain uses the Proof of Authority consensus algorithm.
   """

   def __init__(self, difficulty=2, consensus_type='poa'):
      """
      Initializes the blockchain with a specified difficulty and consensus type.
      :param difficulty: The difficulty level for mining blocks (default is 2).
      :param consensus_type: The type of consensus algorithm to use (default is 'poa').
      """
      self.difficulty = difficulty
      self.unconfirmed_transactions = []
      self.chain = []

      if consensus_type == 'poa':
         self.consensus = ProofOfAuthority()
      
      self.create_genesis_block()
   
   def create_genesis_block(self):
      """
      Creates the genesis block (the first block in the blockchain).
      This block has an index of 0, no transactions, and a previous hash of '0'.
      """
      genesis_block = Block(
         index=0,
         transactions=[],
         timestamp=time.time(),
         previous_hash='0'
      )
      genesis_block.hash = genesis_block.compute_hash()
      self.chain.append(genesis_block)
   
   @property
   def last_block(self):
      """
      Returns the last block in the blockchain.
      :return: The last Block instance in the chain.
      """
      return self.chain[-1]
   
   def add_block(self, block, proof):
      """
      Adds a new block to the blockchain after validating it.
      :param block: The Block instance to add.
      :param proof: The proof of work for the block.
      :return: True if the block is added successfully, False otherwise.
      """
      previous_hash = self.last_block.hash

      if previous_hash != block.previous_hash:
         return False
      
      if not self.is_valid_proof(block, proof):
         return False
      
      block.hash = proof
      self.chain.append(block)
      return True
   
   def is_valid_proof(self, block, block_hash):
      """
      Validates the proof of work for a block.
      :param block: The Block instance to validate.
      :param block_hash: The hash of the block to check.
      :return: True if the proof is valid, False otherwise.
      """
      return (block_hash.startswith('0' * self.difficulty) and
              block_hash == block.compute_hash())
   
   def proof_of_work(self, block):
      """
      Performs the proof of work algorithm to find a valid hash for the block.
      :param block: The Block instance to mine.
      :return: The valid hash for the block.
      """
      block.nonce = 0
      computed_hash = block.compute_hash()

      while not computed_hash.startswith('0' * self.difficulty):
         block.nonce += 1
         computed_hash = block.compute_hash()
      
      return computed_hash
   
   def add_new_transaction(self, transaction):
      """
      Adds a new transaction to the list of unconfirmed transactions.
      :param transaction: The transaction to add (should be a dictionary).
      """
      self.unconfirmed_transactions.append(transaction)
      return len(self.unconfirmed_transactions) - 1
   
   def mine(self, validator_key=None):
      """
      Mines a new block with the current unconfirmed transactions.
      :param validator_key: The public key of the validator (optional for PoA).
      :return: The newly mined Block instance or None if mining failed.
      """
      if not self.unconfirmed_transactions:
         return None
      
      if hasattr(self.consensus, 'is_authorized_validator'):
         if not self.consensus.is_authorized_validator(validator_key):
            raise PermissionError("Validator is not authorized to mine blocks.")
      
      last_block = self.last_block

      new_block = Block(
         index=last_block.index + 1,
         transactions=self.unconfirmed_transactions.copy(),
         timestamp=time.time(),
         previous_hash=last_block.hash
      )

      if hasattr(self.consensus, 'validate_block'):
         proof = self.consensus.validate_block(new_block, validator_key)
      else:
         proof = self.proof_of_work(new_block)
      
      self.add_block(new_block, proof)
      self.unconfirmed_transactions = []
      return new_block.index
   
   def get_validated_logements(self):
      """
      Returns a list of validated logements (transactions) from the blockchain.
      :return: A list of dictionaries representing validated logements.
      """
      validated_logements = []
      
      for block in self.chain[1:]:
         for transaction in block.transactions:
            if transaction.get('status') == 'validated':
               validated_logements.append({
                  'transaction': transaction,
                  'block_index': block.index,
                  'block_timestamp': block.timestamp,
                  'block_hash': block.hash
               })
      
      return validated_logements
   
   def get_chain_data(self):
      """
      Returns the blockchain data as a list of dictionaries.
      :return: A list of dictionaries representing the blockchain.
      """
      return [block.to_dict() for block in self.chain]
   
   @classmethod
   def validate_chain(cls, chain_data):
      """
      Validates the entire blockchain data.
      :param chain_data: A list of dictionaries representing the blockchain.
      :return: True if the chain is valid, False otherwise.
      """
      if len(chain_data) == 0:
         return False
      
      if chain_data[0]['index'] != 0 or chain_data[0]['previous_hash'] != '0':
         return False
      
      for i in range(1, len(chain_data)):
         current_block = Block.from_dict(chain_data[i])
         previous_block = Block.from_dict(chain_data[i - 1])

         if current_block.previous_hash != previous_block.hash:
            return False
         
         if current_block.hash != current_block.compute_hash():
            return False
      
      return True