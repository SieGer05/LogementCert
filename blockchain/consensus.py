import time
from Crypto.signature import SignatureManager

class ProofOfAuthority:
   """
   A class to implement the Proof of Authority (PoA) consensus algorithm.
   This algorithm is based on a set of trusted validators who create new blocks.
   """

   def __init__(self):
      self.authorized_validators = set()
      self.signature_manager = SignatureManager()

   def add_validator(self, public_key_pem):
      """
      Adds a new validator to the set of authorized validators.
      :param public_key_pem: The public key of the validator in PEM format.
      """
      self.authorized_validators.add(public_key_pem)

   def remove_validator(self, public_key_pem):
      """
      Removes a validator from the set of authorized validators.
      :param public_key_pem: The public key of the validator in PEM format.
      """
      self.authorized_validators.discard(public_key_pem)
   
   def is_authorized_validator(self, public_key_pem):
      """
      Checks if a given public key belongs to an authorized validator.
      :param public_key_pem: The public key of the validator in PEM format.
      :return: True if the validator is authorized, False otherwise.
      """
      return public_key_pem in self.authorized_validators
   
   def validate_block(self, block, validator_public_key_pem):
      """
      Validates a block by checking if it was signed by an authorized validator.
      :param block: The block to validate.
      :param validator_public_key_pem: The public key of the validator who signed the block.
      :return: True if the block is valid, False otherwise.
      """
      if not self.is_authorized_validator(validator_public_key_pem):
         return PermissionError("Validator is not authorized.")
      
      return block.compute_hash()
   
   def get_validators(self):
      """
      Returns the list of authorized validators.
      :return: A set of public keys of authorized validators.
      """
      return self.authorized_validators