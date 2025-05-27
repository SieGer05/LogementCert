import os
import json
from hashlib import sha256
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

class KeyManager:
   """Manage RSA key generation, saving, and loading."""

   def __init__(self, keys_directory='keys'):
      self.keys_directory = keys_directory
      os.makedirs(keys_directory, exist_ok=True)

   def generate_key_pair(self, key_size=2048):
      private_key = rsa.generate_private_key(
         public_exponent=65537,
         key_size=key_size
      )
      public_key = private_key.public_key()

      private_pem = private_key.private_bytes(
         encoding=serialization.Encoding.PEM,
         format=serialization.PrivateFormat.PKCS8,
         encryption_algorithm=serialization.NoEncryption()
      ).decode('utf-8')

      public_pem = public_key.public_bytes(
         encoding=serialization.Encoding.PEM,
         format=serialization.PublicFormat.SubjectPublicKeyInfo
      ).decode('utf-8')

      key_id = self.get_key_fingerprint(public_pem)

      return private_pem, public_pem, key_id

   def save_key_pair(self, private_key_pem, public_key_pem, key_id=None):
      if key_id is None:
         key_id = self.get_key_fingerprint(public_key_pem)

      private_path = os.path.join(self.keys_directory, f'{key_id}_private.pem')
      public_path = os.path.join(self.keys_directory, f'{key_id}_public.pem')

      with open(private_path, 'w') as f:
         f.write(private_key_pem)

      with open(public_path, 'w') as f:
         f.write(public_key_pem)

      os.chmod(private_path, 0o600)

      return key_id, private_path, public_path

   def load_private_key(self, file_path):
      with open(file_path, 'r') as f:
         return f.read()

   def load_public_key(self, file_path):
      with open(file_path, 'r') as f:
         return f.read()

   def get_key_fingerprint(self, public_key_pem):
      """Calculate a SHA256 fingerprint truncated to 16 hex characters."""
      return sha256(public_key_pem.encode('utf-8')).hexdigest()[:16]

   def load_all_public_keys(self):
      """Load all public keys from keys_directory into a dict {key_id: public_key_pem}."""
      public_keys = {}
      for filename in os.listdir(self.keys_directory):
         if filename.endswith('_public.pem'):
            path = os.path.join(self.keys_directory, filename)
            pub_key = self.load_public_key(path)
            kid = self.get_key_fingerprint(pub_key)
            public_keys[kid] = pub_key
      return public_keys

   def export_public_keys(self, output_file='public_keys.json'):
      public_keys = self.load_all_public_keys()
      output_path = os.path.join(self.keys_directory, output_file)
      with open(output_path, 'w') as f:
         json.dump(public_keys, f, indent=2)
      return output_path