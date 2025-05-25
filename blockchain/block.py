import json
import time
from hashlib import sha256

class Block:
   """A class representing a block in a blockchain."""
   
   def __init__(self, index, transactions, timestamp, previous_hash, nonce=0):
      """
      Initializes a new block with the given parameters.
      :param index: The index of the block in the blockchain.
      :param transactions: A list of transactions included in the block.
      :param timestamp: The time when the block was created.
      :param previous_hash: The hash of the previous block in the blockchain.
      :param nonce: A number used for the proof-of-work algorithm (default is 0).
      """
      self.index = index
      self.transactions = transactions
      self.timestamp = timestamp
      self.previous_hash = previous_hash
      self.nonce = nonce
      self.hash = None

   def compute_hash(self):
      """
      Computes the hash of the block using SHA-256.
      :return: The hash of the block as a hexadecimal string.
      """
      block_data = {
         'index': self.index,
         'transactions': self.transactions,
         'timestamp': self.timestamp,
         'previous_hash': self.previous_hash,
         'nonce': self.nonce
      }
      block_string = json.dumps(block_data, sort_keys=True)
      return sha256(block_string.encode()).hexdigest()
   
   def to_dict(self):
      """
      Converts the block to a dictionary representation.
      :return: A dictionary containing the block's data.
      """
      return {
         'index': self.index,
         'transactions': self.transactions,
         'timestamp': self.timestamp,
         'previous_hash': self.previous_hash,
         'nonce': self.nonce,
         'hash': self.hash
      }
   
   @classmethod
   def from_dict(cls, data):
      """
      Creates a Block instance from a dictionary representation.
      :param data: A dictionary containing the block's data.
      :return: An instance of the Block class.
      """
      
      block = cls(
         data['index'],
         data['transactions'],
         data['timestamp'],
         data['previous_hash'],
         data['nonce']
      )
      block.hash = data.get('hash')
      return block