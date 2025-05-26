import json
import time
from hashlib import sha256


class Block:
   """A class representing a block in a blockchain."""

   def __init__(self, index, transactions, timestamp, previous_hash, nonce=0, validator=None, signature=None):
      """
      Initializes a new block.
      
      :param index: Block index in the chain
      :param transactions: List of transactions in this block
      :param timestamp: Block creation timestamp
      :param previous_hash: Hash of the previous block
      :param nonce: Nonce for Proof of Work
      :param validator: Public key PEM string of the validator (for PoA)
      :param signature: Base64-encoded signature (for PoA)
      """
      self.index = index
      self.transactions = transactions
      self.timestamp = timestamp
      self.previous_hash = previous_hash
      self.nonce = nonce
      self.hash = None
      self.validator = validator  # Public key PEM string
      self.signature = signature  # Base64-encoded signature

   def compute_hash(self):
      """
      Computes SHA-256 hash of the block's content (excluding the signature).
      This ensures signature verification works correctly.
      """
      block_data = {
         'index': self.index,
         'transactions': self.transactions,
         'timestamp': self.timestamp,
         'previous_hash': self.previous_hash,
         'nonce': self.nonce,
         'validator': self.validator
      }
      block_string = json.dumps(block_data, sort_keys=True)
      return sha256(block_string.encode()).hexdigest()

   def to_dict(self):
      """
      Converts the block to a dictionary (used for storage or JSON serialization).
      """
      return {
         'index': self.index,
         'transactions': self.transactions,
         'timestamp': self.timestamp,
         'previous_hash': self.previous_hash,
         'nonce': self.nonce,
         'hash': self.hash,
         'validator': self.validator,
         'signature': self.signature
      }

   @classmethod
   def from_dict(cls, data):
      """
      Reconstructs a Block object from a dictionary.
      
      :param data: Dictionary containing block data
      :return: Block instance
      """
      block = cls(
         data['index'],
         data['transactions'],
         data['timestamp'],
         data['previous_hash'],
         data.get('nonce', 0),
         data.get('validator'),
         data.get('signature')
      )
      block.hash = data.get('hash')
      return block

   def __str__(self):
      """String representation of the block."""
      return f"Block(index={self.index}, hash={self.hash[:10]}..., transactions={len(self.transactions)})"

   def __repr__(self):
      """Debug representation of the block."""
      return self.__str__()