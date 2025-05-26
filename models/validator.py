from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime
import hashlib


@dataclass
class Validator:
   """
   Represents a validator (local authority) in the LogementCert system.
   Validators are entities authorized to certify housing
   in their geographical jurisdiction.
   """
   
   name: str
   organization: str 
   
   
   # Cryptographic keys
   public_key_pem: str
   
   # Geographic jurisdiction
   city: str
   region: str
   country: str
   jurisdiction_type: str  # "municipal", "regional", "national"
   
   # Contact information
   contact_email: str
   contact_phone: Optional[str] = None
   office_address: Optional[str] = None
   
   # Status and permissions
   is_active: bool = True
   authority_level: int = 1  # 1=local, 2=regional, 3=national
   max_certifications_per_day: int = 50
   
   # Specializations
   authorized_property_types: List[str] = field(default_factory=lambda: ["apartment", "house", "room", "studio"])
   specializations: List[str] = field(default_factory=list)  # "tourism", "student_housing", etc.
   
   # Metadata
   created_at: datetime = field(default_factory=datetime.now)
   last_activity: Optional[datetime] = None
   total_certifications: int = 0
   
   def __post_init__(self):
      """Validation after initialization"""
      self.validate()
      
   def validate(self) -> bool:
      """Validates validator data"""
      errors = []
      
      if not self.name or len(self.name) < 2:
         errors.append("Name must contain at least 2 characters")
      
      if not self.public_key_pem or "BEGIN PUBLIC KEY" not in self.public_key_pem:
         errors.append("Invalid PEM public key")
      
      if self.jurisdiction_type not in ["municipal", "regional", "national"]:
         errors.append("Invalid jurisdiction type")
      
      if not self.contact_email or "@" not in self.contact_email:
         errors.append("Invalid contact email")
      
      if self.authority_level not in [1, 2, 3]:
         errors.append("Invalid authority level (1-3)")
      
      if self.max_certifications_per_day <= 0:
         errors.append("max_certifications_per_day must be positive")
      
      if errors:
         raise ValueError(f"Validation errors: {', '.join(errors)}")
      
      return True
   
   def get_validator_id(self) -> str:
      """Generates a unique ID based on the public key"""
      # Uses the first 16 characters of the SHA-256 hash of the public key
      hash_object = hashlib.sha256(self.public_key_pem.encode())
      return hash_object.hexdigest()[:16]
   
   def can_certify_property_type(self, property_type: str) -> bool:
      """Checks if the validator can certify this property type"""
      return property_type in self.authorized_property_types
   
   def can_certify_in_location(self, city: str, country: str) -> bool:
      """Checks if the validator can certify in this location"""
      if self.jurisdiction_type == "national":
         return country.lower() == self.country.lower()
      elif self.jurisdiction_type == "regional":
         return (country.lower() == self.country.lower() and 
            city.lower() in self.region.lower())
      else:  # municipal
         return (country.lower() == self.country.lower() and 
            city.lower() == self.city.lower())
   
   def can_certify_today(self) -> bool:
      """Checks if the validator can still certify today"""
      if not self.is_active:
         return False
      
      return True
   
   def record_certification(self):
      """Records a new certification"""
      self.total_certifications += 1
      self.last_activity = datetime.now()
   
   def deactivate(self, reason: str = ""):
      """Deactivates the validator"""
      self.is_active = False
      self.last_activity = datetime.now()
   
   def reactivate(self):
      """Reactivates the validator"""
      self.is_active = True
      self.last_activity = datetime.now()
   
   def get_jurisdiction_display(self) -> str:
      """Returns the jurisdiction in readable form"""
      if self.jurisdiction_type == "municipal":
         return f"{self.city}, {self.country}"
      elif self.jurisdiction_type == "regional":
         return f"{self.region}, {self.country}"
      else:
         return self.country
   
   def get_stats(self) -> Dict[str, Any]:
      """Returns validator statistics"""
      return {
         "validator_id": self.get_validator_id(),
         "name": self.name,
         "organization": self.organization,
         "jurisdiction": self.get_jurisdiction_display(),
         "is_active": self.is_active,
         "total_certifications": self.total_certifications,
         "last_activity": self.last_activity.isoformat() if self.last_activity else None,
         "authorized_types": self.authorized_property_types,
         "specializations": self.specializations
      }
   
   def to_dict(self) -> Dict[str, Any]:
      """Converts to dictionary for JSON serialization"""
      return {
         "name": self.name,
         "organization": self.organization,
         "public_key_pem": self.public_key_pem,
         "city": self.city,
         "region": self.region,
         "country": self.country,
         "jurisdiction_type": self.jurisdiction_type,
         "contact_email": self.contact_email,
         "contact_phone": self.contact_phone,
         "office_address": self.office_address,
         "is_active": self.is_active,
         "authority_level": self.authority_level,
         "max_certifications_per_day": self.max_certifications_per_day,
         "authorized_property_types": self.authorized_property_types,
         "specializations": self.specializations,
         "created_at": self.created_at.isoformat(),
         "last_activity": self.last_activity.isoformat() if self.last_activity else None,
         "total_certifications": self.total_certifications
      }
   
   @classmethod
   def from_dict(cls, data: Dict[str, Any]) -> 'Validator':
      """Creates a validator from a dictionary"""
      validator = cls(
         name=data["name"],
         organization=data["organization"],
         public_key_pem=data["public_key_pem"],
         city=data["city"],
         region=data["region"],
         country=data["country"],
         jurisdiction_type=data["jurisdiction_type"],
         contact_email=data["contact_email"],
         contact_phone=data.get("contact_phone"),
         office_address=data.get("office_address"),
         is_active=data.get("is_active", True),
         authority_level=data.get("authority_level", 1),
         max_certifications_per_day=data.get("max_certifications_per_day", 50),
         authorized_property_types=data.get("authorized_property_types", ["apartment", "house", "room", "studio"]),
         specializations=data.get("specializations", []),
         created_at=datetime.fromisoformat(data.get("created_at", datetime.now().isoformat())),
         total_certifications=data.get("total_certifications", 0)
      )
      
      if data.get("last_activity"):
         validator.last_activity = datetime.fromisoformat(data["last_activity"])
      
      return validator
   
   def get_contact_info(self) -> Dict[str, str]:
      """Returns contact information"""
      contact = {
         "email": self.contact_email,
         "organization": self.organization
      }
      
      if self.contact_phone:
         contact["phone"] = self.contact_phone
      
      if self.office_address:
         contact["address"] = self.office_address
      
      return contact
   
   def __str__(self) -> str:
      """Text representation of the validator"""
      status = "Active" if self.is_active else "Inactive"
      return f"{self.name} ({self.organization}) - {self.get_jurisdiction_display()} [{status}]"
   
   def __repr__(self) -> str:
      """Debug representation"""
      return f"Validator(name={self.name}, city={self.city}, active={self.is_active})"