import json
import base64
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.exceptions import InvalidSignature

class SignatureManager:
   """Manage digital signatures using RSA keys."""

   def sign_data(self, data, private_key_pem):
      try:
         # Load private key object from PEM
         private_key = serialization.load_pem_private_key(
               private_key_pem.encode('utf-8'),
               password=None
         )

         # Convert data to JSON bytes if dict, else encode string bytes
         if isinstance(data, dict):
               data_bytes = json.dumps(data, sort_keys=True).encode('utf-8')
         else:
               data_bytes = str(data).encode('utf-8')

         # Sign data bytes with PSS padding and SHA256 hash
         signature = private_key.sign(
               data_bytes,
               padding.PSS(
                  mgf=padding.MGF1(hashes.SHA256()),
                  salt_length=padding.PSS.MAX_LENGTH
               ),
               hashes.SHA256()
         )

         # Encode signature in base64 string
         return base64.b64encode(signature).decode('utf-8')

      except Exception as e:
         raise ValueError(f"Error signing data: {e}")

   def verify_signature(self, data, signature_b64, public_key_pem):
      try:
         # Load public key object from PEM
         public_key = serialization.load_pem_public_key(
               public_key_pem.encode('utf-8')
         )
         # Decode signature from base64 string
         signature = base64.b64decode(signature_b64.encode('utf-8'))

         # Convert data to bytes (JSON if dict, else string)
         if isinstance(data, dict):
               data_bytes = json.dumps(data, sort_keys=True).encode('utf-8')
         else:
               data_bytes = str(data).encode('utf-8')

         # Verify signature with PSS padding and SHA256 hash
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

   def create_message_signature(self, message, private_key_pem, key_id=None, metadata=None):
      # Prepare the message with timestamp and optional metadata for signing
      full_data = {
         'message': message,
         'timestamp': time.time(),
         'metadata': metadata or {}
      }
      # Sign only the 'message' field (you can adjust if you want to sign full_data)
      signature = self.sign_data(message, private_key_pem)
      return {
         'data': full_data,
         'signature': signature,
         'key_id': key_id
      }

   def verify_message_signature(self, signed_message, public_key_pem):
      try:
         # Extract original message and signature to verify
         message = signed_message['data']['message']
         signature = signed_message['signature']
         return self.verify_signature(message, signature, public_key_pem)
      except KeyError:
         return False

   def batch_verify_signatures(self, signed_messages, public_keys):
      # Verify a list of signed messages given a dict of public keys {key_id: public_key_pem}
      results = []
      for signed_message in signed_messages:
         key_id = signed_message.get('key_id')
         if key_id and key_id in public_keys:
            public_key = public_keys[key_id]
            valid = self.verify_message_signature(signed_message, public_key)
            results.append(valid)
         else:
            results.append(False)
      return results