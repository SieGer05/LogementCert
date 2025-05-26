import time
import json
from .block import Block
from .consensus import ProofOfAuthority


class LogementBlockchain:
   """
   Blockchain for managing housing (logement) transactions.
   Supports Proof of Authority (PoA) and Proof of Work (PoW) consensus.
   """

   def __init__(self, difficulty=2, consensus_type='poa'):
      """
      Initialize the blockchain.
      
      :param difficulty: Mining difficulty for PoW
      :param consensus_type: 'poa' for Proof of Authority, 'pow' for Proof of Work
      """
      self.difficulty = difficulty
      self.chain = []
      self.unconfirmed_transactions = []
      self.consensus_type = consensus_type.lower()

      if self.consensus_type == 'poa':
         self.consensus = ProofOfAuthority()
      else:
         self.consensus = None 

      self._create_genesis_block()

   def _create_genesis_block(self):
      """Creates the first block of the chain (genesis block)."""
      genesis_block = Block(
         index=0,
         transactions=[],
         timestamp=time.time(),
         previous_hash="0"
      )
      genesis_block.hash = genesis_block.compute_hash()
      self.chain.append(genesis_block)

   @property
   def last_block(self):
      """Returns the latest block in the chain."""
      return self.chain[-1]

   def add_block(self, block, proof):
      """
      Adds a validated block to the chain.
      
      :param block: Block instance to add
      :param proof: Valid hash of the block
      :return: True if added, False otherwise
      """
      if block.previous_hash != self.last_block.hash:
         print(f"Previous hash mismatch: expected {self.last_block.hash}, got {block.previous_hash}")
         return False

      if self.consensus_type == 'poa' and block.signature:
         try:
            self.consensus.validate_block(block)
            self.chain.append(block)
            return True
         except (ValueError, PermissionError) as e:
            print(f"PoA validation failed: {e}")
            return False
      
      if not self._is_valid_proof(block, proof):
         print(f"Invalid proof for block: {proof}")
         return False

      block.hash = proof
      self.chain.append(block)
      return True

   def _is_valid_proof(self, block, block_hash):
      """
      Validates block hash against difficulty level.
      
      :param block: Block instance
      :param block_hash: Hash to validate
      :return: True if valid, False otherwise
      """
      expected_hash = block.compute_hash()
      return (block_hash.startswith('0' * self.difficulty) and block_hash == expected_hash)

   def proof_of_work(self, block):
      """
      Performs PoW to compute a valid block hash.
      
      :param block: Block to mine
      :return: Valid hash
      """
      block.nonce = 0
      computed_hash = block.compute_hash()
      while not computed_hash.startswith('0' * self.difficulty):
         block.nonce += 1
         computed_hash = block.compute_hash()
      return computed_hash

   def add_new_transaction(self, transaction):
      """
      Queues a new transaction to be added to the next block.
      
      :param transaction: dict representing the transaction
      :return: Index of the transaction in the unconfirmed list
      """
      if 'timestamp' not in transaction:
         transaction['timestamp'] = time.time()
         
      self.unconfirmed_transactions.append(transaction)
      return len(self.unconfirmed_transactions) - 1

   def mine(self, private_key_pem=None):
      if not self.unconfirmed_transactions:
         return None

      new_block = Block(
         index=self.last_block.index + 1,
         transactions=self.unconfirmed_transactions.copy(),
         timestamp=time.time(),
         previous_hash=self.last_block.hash
      )

      if self.consensus_type == 'poa':
         if not private_key_pem:
               print("PoA mining requires private key for signing")
               return None
         try:
               signed_block = self.consensus.sign_block(new_block, private_key_pem)
               added = self.add_block(signed_block, signed_block.hash)  
         except (ValueError, PermissionError) as e:
               print(f"PoA signing failed: {e}")
               return None
      else:
         proof = self.proof_of_work(new_block)
         added = self.add_block(new_block, proof)

      if added:
         self.unconfirmed_transactions.clear()
         return new_block.index
      return None

   def get_validated_logements(self):
      """
      Retrieves all validated logement transactions.
      
      :return: List of dicts with validated logements and block metadata
      """
      validated = []
      for block in self.chain[1:]:  
         for tx in block.transactions:
            if tx.get('status') == 'validated':
               validated.append({
                  'transaction': tx,
                  'block_index': block.index,
                  'block_timestamp': block.timestamp,
                  'block_hash': block.hash
               })
      return validated

   def get_transactions_by_address(self, address):
      """
      Get all transactions involving a specific address.
      
      :param address: Address to search for
      :return: List of transactions
      """
      transactions = []
      for block in self.chain[1:]: 
         for tx in block.transactions:
            if tx.get('from') == address or tx.get('to') == address:
               transactions.append({
                  'transaction': tx,
                  'block_index': block.index,
                  'block_timestamp': block.timestamp,
                  'block_hash': block.hash
                  })
      return transactions

   def get_chain_data(self):
      """Returns full blockchain as a list of dicts."""
      return [block.to_dict() for block in self.chain]

   def get_chain_stats(self):
      """Returns statistics about the blockchain."""
      total_transactions = sum(len(block.transactions) for block in self.chain[1:])
      validated_transactions = len(self.get_validated_logements())
      
      return {
         'total_blocks': len(self.chain),
         'total_transactions': total_transactions,
         'validated_transactions': validated_transactions,
         'pending_transactions': len(self.unconfirmed_transactions),
         'consensus_type': self.consensus_type,
         'difficulty': self.difficulty,
         'last_block_hash': self.last_block.hash,
         'validators_count': len(self.consensus.get_validators()) if self.consensus_type == 'poa' else 0
      }

   def add_validator(self, public_key_pem):
      """Add a new authorized validator."""
      if self.consensus_type != 'poa':
         raise NotImplementedError("Validators only supported in PoA mode")
      self.consensus.add_validator(public_key_pem)

   def remove_validator(self, public_key_pem):
      """Remove an authorized validator."""
      if self.consensus_type != 'poa':
         raise NotImplementedError("Validators only supported in PoA mode")
      self.consensus.remove_validator(public_key_pem)

   def get_validators(self):
      """Get list of authorized validators."""
      if self.consensus_type != 'poa':
         return set()
      return self.consensus.get_validators()

   def is_validator_authorized(self, public_key_pem):
      """Check if a validator is authorized."""
      if self.consensus_type != 'poa':
         return False
      return self.consensus.is_authorized_validator(public_key_pem)

   @classmethod
   def validate_chain(cls, chain_data):
      """
      Validates the integrity of a full chain.
      
      :param chain_data: List of dicts representing the blockchain
      :return: True if valid, False otherwise
      """
      if not chain_data or chain_data[0]['index'] != 0 or chain_data[0]['previous_hash'] != '0':
         return False

      for i in range(1, len(chain_data)):
         curr = Block.from_dict(chain_data[i])
         prev = Block.from_dict(chain_data[i - 1])

         if curr.previous_hash != prev.hash:
               return False
         if curr.hash != curr.compute_hash():
               return False

      return True

   def export_chain(self, filename):
      """
      Export blockchain to JSON file.
      
      :param filename: Output filename
      """
      chain_data = self.get_chain_data()
      with open(filename, 'w') as f:
         json.dump(chain_data, f, indent=2)

   @classmethod
   def import_chain(cls, filename, difficulty=2, consensus_type='poa'):
      """
      Import blockchain from JSON file.
      
      :param filename: Input filename
      :param difficulty: Mining difficulty
      :param consensus_type: Consensus type
      :return: LogementBlockchain instance
      """
      with open(filename, 'r') as f:
         chain_data = json.load(f)
      
      if not cls.validate_chain(chain_data):
         raise ValueError("Invalid chain data")
      
      blockchain = cls(difficulty=difficulty, consensus_type=consensus_type)
      blockchain.chain = [Block.from_dict(block_data) for block_data in chain_data]
      
      return blockchain