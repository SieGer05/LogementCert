from blockchain.blockchain import LogementBlockchain

class BlockchainService:
   def __init__(self):
      self.blockchain = LogementBlockchain(consensus_type="poa")

   def add_validator(self, key_pem: str):
      self.blockchain.add_validator(key_pem)

   def add_new_transaction(self, transaction: dict):
      self.blockchain.add_new_transaction(transaction)

   def get_transactions_by_address(self, owner: str):
      return self.blockchain.get_transactions_by_address(owner)

   def get_validated_logements(self):
      return self.blockchain.get_validated_logements()

   def get_chain_stats(self):
      return self.blockchain.get_chain_stats()

   def mine_transaction(self, transaction: dict, private_key: str):
      return self.blockchain.mine_transaction(transaction, private_key)

   @property
   def unconfirmed_transactions(self):
      return self.blockchain.unconfirmed_transactions

# Singleton instance
blockchain_service = BlockchainService()