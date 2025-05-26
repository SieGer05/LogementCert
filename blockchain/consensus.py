import json
from crypto import SignatureManager

class ProofOfAuthority:
   """
   Implements Proof of Authority consensus with cryptographic validation.
   """

   def __init__(self):
      self.authorized_validators = set()
      self.signature_manager = SignatureManager()

   def add_validator(self, public_key_pem):
      """
      Add a validator to the authorized list.
      
      :param public_key_pem: Public key in PEM format
      """
      if not isinstance(public_key_pem, str):
         raise ValueError("Public key must be a string in PEM format")
      self.authorized_validators.add(public_key_pem)

   def remove_validator(self, public_key_pem):
      """
      Remove a validator from the authorized list.
      
      :param public_key_pem: Public key in PEM format
      """
      self.authorized_validators.discard(public_key_pem)

   def is_authorized_validator(self, public_key_pem):
      """
      Check if a validator is authorized.
      
      :param public_key_pem: Public key in PEM format
      :return: True if authorized, False otherwise
      """
      return public_key_pem in self.authorized_validators

   def sign_block(self, block, private_key_pem):
      """
      Signs the block's hash using the private key and attaches the signature.
      
      :param block: Block instance to sign
      :param private_key_pem: Private key in PEM format
      :return: The signed block
      """
      if not private_key_pem:
         raise ValueError("Private key is required for signing")
               
      public_key_pem = self.signature_manager.get_public_key_pem_from_private(private_key_pem)
      
      if not self.is_authorized_validator(public_key_pem):
         raise PermissionError("Validator is not authorized")
      
      block.validator = public_key_pem
      block.hash = block.compute_hash()
      
      signature = self.signature_manager.sign_data(block.hash, private_key_pem)
      block.signature = signature
      
      return block

   def validate_block(self, block):
      """
      Validates the block by verifying its signature and the validator's authorization.
      
      :param block: Block instance to validate
      :return: True if valid
      :raises: ValueError or PermissionError if validation fails
      """
      if not block.validator or not block.signature:
         raise ValueError("Block missing validator identity or signature")
      
      if not self.is_authorized_validator(block.validator):
         raise PermissionError("Validator is not authorized")
      
      if not self.signature_manager.verify_signature(block.hash, block.signature, block.validator):
         raise ValueError("Invalid block signature")
      
      return True

   def get_validators(self):
      """
      Get the set of authorized validators.
      
      :return: Set of public key PEMs
      """
      return self.authorized_validators.copy()

   def get_validator_count(self):
      """
      Get the number of authorized validators.
      
      :return: Number of validators
      """
      return len(self.authorized_validators)