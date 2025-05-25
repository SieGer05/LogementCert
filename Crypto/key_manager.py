import os
import json
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

class KeyManager:
   """Manages the generation, storage, and retrieval of RSA keys for digital signatures."""

   def __init__(self, keys_directory='keys'):
      """
      Initializes the KeyManager with a specified directory for storing keys.
      :param keys_directory: Directory where keys will be stored.
      """
      self.keys_directory = keys_directory
      os.makedirs(keys_directory, exist_ok=True)
   
   def generate_key_pair(self, key_size=2048):
      """
      Generates a new RSA key pair.
      :param key_size: Size of the RSA key to generate (default is 2048 bits).
      :return: A tuple containing the private and public keys.
      """
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

      return private_pem, public_pem
   
   def save_key_pair(self, private_key, public_key, identifier):
      """
      Saves the RSA key pair to files.
      :param private_key: The private key in PEM format.
      :param public_key: The public key in PEM format.
      :param identifier: Unique identifier for the key pair (e.g., username).
      """
      private_path = os.path.join(self.keys_directory, f'{identifier}_private.pem')
      public_path = os.path.join(self.keys_directory, f'{identifier}_public.pem')

      with open(private_path, 'w') as private_file:
         private_file.write(private_key)
      
      with open(public_path, 'w') as public_file:
         public_file.write(public_key)

      os.chmod(private_path, 0o600)

      return private_path, public_path
   
   def load_private_key(self, file_path):
      """
      Loads a private key from a file.
      :param file_path: Path to the private key file.
      :return: The private key PEM format.
      """
      with open(file_path, 'r') as key_file:
         return key_file.read()
      
   def load_public_key(self, file_path):
      """
      Loads a public key from a file.
      :param file_path: Path to the public key file.
      :return: The public key PEM format.
      """
      with open(file_path, 'r') as key_file:
         return key_file.read()
   
   def export_public_keys(self, output_file='public_keys.json'):
      """
      Exports all public keys in the keys directory to a JSON file.
      :param output_file: The name of the output JSON file.
      """
      public_keys = {}

      for filename in os.listdir(self.keys_directory):
         if filename.endswith('_public.pem'):
            identifier = filename.replace('_public.pem', '')
            filepath = os.path.join(self.keys_directory, filename)
            public_keys[identifier] = self.load_public_key(filepath)

      output_path = os.path.join(self.keys_directory, output_file)
      with open(output_path, 'w') as json_file:
         json.dump(public_keys, json_file, indent=2)
      
      return output_path
   
   def get_key_fingerprint(self, public_key_pem):
      """
      Computes a fingerprint for a public key.
      :param public_key: The public key in PEM format.
      :return: A fingerprint of the public key.
      """
      from hashlib import sha256
      return sha256(public_key_pem.encode()).hexdigest()[:16]
   
   def load_all_public_keys(self):
      """Charge toutes les clés publiques et renvoie un dict {key_id: clé_publique}."""
      public_keys = {}
      for filename in os.listdir(self.keys_directory):
         if filename.endswith('_public.pem'):
            filepath = os.path.join(self.keys_directory, filename)
            pub_key = self.load_public_key(filepath)
            kid = self.get_key_fingerprint(pub_key)
            public_keys[kid] = pub_key
      return public_keys