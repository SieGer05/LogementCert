import json
import base64
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.exceptions import InvalidSignature

class SignatureManager:
   """Manages digital signatures for data integrity and authenticity using RSA keys."""

   def __init__(self):
      """
      Initializes the SignatureManager.
      """
      pass

   def sign_data(self, data, private_key_pem):
      """
      Signs the given data using the provided RSA private key.
      :param data: The data to be signed (can be a dictionary or string).
      :param private_key_pem: The RSA private key in PEM format.
      :return: The digital signature as a base64 encoded string.
      """
      try:
         private_key = serialization.load_pem_private_key(
            private_key_pem.encode('utf-8'),
            password=None
         )

         if isinstance(data, dict):
            data_bytes = json.dumps(data, sort_keys=True).encode('utf-8')
         else:
            data_bytes = str(data).encode('utf-8')
         
         signature = private_key.sign(
            data_bytes,
            padding.PSS(
               mgf=padding.MGF1(hashes.SHA256()),
               salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
         )

         return base64.b64encode(signature).decode('utf-8')
      
      except Exception as e:
         raise ValueError(f"Error signing data: {e}")
   
   def verify_signature(self, data, signature_b64, public_key_pem):
      """
      Verifies the digital signature of the given data using the provided RSA public key.
      :param data: The original data that was signed (can be a dictionary or string).
      :param signature_b64: The digital signature as a base64 encoded string.
      :param public_key_pem: The RSA public key in PEM format.
      :return: True if the signature is valid, False otherwise.
      """
      try:
         public_key = serialization.load_pem_public_key(
            public_key_pem.encode('utf-8')
         )

         signature = base64.b64decode(signature_b64.encode('utf-8'))

         if isinstance(data, dict):
            data_bytes = json.dumps(data, sort_keys=True).encode('utf-8')
         else:
            data_bytes = str(data).encode('utf-8')
         
         public_key.verify(
            signature,
            data_bytes,
            padding.PSS(
               mgf=padding.MGF1(hashes.SHA256()),
               salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
         )

         return True
      
      except InvalidSignature:
         return False
      except Exception:
         return False
   
   def create_message_signature(self, message, private_key_pem, metadata=None):
      """
      Creates a signed message with optional metadata.
      :param message: The message to be signed.
      :param private_key_pem: The RSA private key in PEM format.
      :param metadata: Optional metadata to include in the signature.
      :return: A dictionary containing the signed message and metadata.
      """
      import time

      full_data = {
         'message': message,
         'timestamp': time.time(),
         'metadata': metadata or {}
      }
      
      signature = self.sign_data(message, private_key_pem)

      return {
         'data': full_data,
         'signature': signature
      }

   def verify_message_signature(self, signed_message, public_key_pem):
      """
      Verifies a signed message and its metadata.
      :param signed_message: The signed message dictionary containing 'data' and 'signature'.
      :param public_key_pem: The RSA public key in PEM format.
      :return: True if the signature is valid, False otherwise.
      """
      try:
         message = signed_message['data']['message']
         signature = signed_message['signature']

         return self.verify_signature(
            message,
            signature,
            public_key_pem
         )
      
      except KeyError:
         return False
      
   def batch_verify_signatures(self, signed_messages, public_keys):
      """
      Batch verifies multiple signed messages against their corresponding public keys.
      :param signed_messages: A list of signed message dictionaries.
      :param public_keys: A dict of RSA public keys in PEM format with key_id as key.
      :return: A list of boolean values indicating the validity of each signature.
      """
      results = []

      for signed_message in signed_messages:
         try:
            key_id = signed_message.get('key_id')
            if key_id and key_id in public_keys:
                  public_key = public_keys[key_id]
                  valid = self.verify_message_signature(signed_message, public_key)
                  results.append(valid)
            else:
                  results.append(False)
         except Exception:
            results.append(False)
      
      return results