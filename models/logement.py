from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime
import time
import uuid


@dataclass
class Logement:   
   property_id: str
   owner_wallet: str
   
   title: str
   address: str
   city: str
   country: str
   postal_code: str
   
   property_type: str 
   max_occupancy: int
   bedrooms: int
   bathrooms: int
   surface_area: float  
   
   price_per_night: float
   currency: str = "EUR"
   
   amenities: List[str] = field(default_factory=list)
   description: str = ""
   house_rules: List[str] = field(default_factory=list)
   
   latitude: Optional[float] = None
   longitude: Optional[float] = None
   
   certification_status: str = "pending"  
   certified_by: Optional[str] = None  
   certification_date: Optional[datetime] = None
   expiry_date: Optional[datetime] = None
   
   created_at: datetime = field(default_factory=datetime.now)
   updated_at: datetime = field(default_factory=datetime.now)
   
   def __post_init__(self):
      """Validation and automatic generation after initialization"""
      if not self.property_id:
         self.property_id = self.generate_property_id()
      
      self.validate()
   
   @staticmethod
   def generate_property_id(prefix: str = "LOG") -> str:
      """Generates a unique ID for the property"""
      timestamp = str(int(time.time()))[-6:]  
      unique_id = str(uuid.uuid4())[:8] 
      return f"{prefix}{timestamp}{unique_id.upper()}"
   
   def validate(self) -> bool:
      """Validates property data"""
      errors = []
      
      if self.max_occupancy <= 0:
         errors.append("max_occupancy must be positive")
      
      if self.price_per_night <= 0:
         errors.append("price_per_night must be positive")
      
      if self.property_type not in ["apartment", "house", "room", "studio", "villa", "other"]:
         errors.append("invalid property_type")
      
      if self.certification_status not in ["pending", "validated", "expired", "revoked"]:
         errors.append("invalid certification_status")
      
      if not self.address or not self.city or not self.country:
         errors.append("address, city and country are required")
      
      if errors:
         raise ValueError(f"Validation errors: {', '.join(errors)}")
      
      return True
   
   def to_transaction(self) -> Dict[str, Any]:
      """
      Converts the property into a blockchain transaction.
      This method formats the data to be stored on the blockchain.
      """
      return {
         "type": "logement_certification",
         "property_id": self.property_id,
         "owner": self.owner_wallet,
         "title": self.title,
         "address": self.address,
         "city": self.city,
         "country": self.country,
         "postal_code": self.postal_code,
         "property_type": self.property_type,
         "max_occupancy": self.max_occupancy,
         "bedrooms": self.bedrooms,
         "bathrooms": self.bathrooms,
         "surface_area": self.surface_area,
         "price_per_night": self.price_per_night,
         "currency": self.currency,
         "amenities": self.amenities,
         "description": self.description,
         "house_rules": self.house_rules,
         "latitude": self.latitude,
         "longitude": self.longitude,
         "status": self.certification_status,
         "created_at": self.created_at.isoformat(),
         "certification_timestamp": time.time()
      }
   
   @classmethod
   def from_transaction(cls, transaction_data: Dict[str, Any]) -> 'Logement':
      """
      Crée un objet Logement à partir d'une transaction blockchain.
      """
      return cls(
         property_id=transaction_data["property_id"],
         owner_wallet=transaction_data["owner"],
         title=transaction_data.get("title", ""),
         address=transaction_data["address"],
         city=transaction_data["city"],
         country=transaction_data["country"],
         postal_code=transaction_data.get("postal_code", ""),
         property_type=transaction_data["property_type"],
         max_occupancy=transaction_data["max_occupancy"],
         bedrooms=transaction_data.get("bedrooms", 1),
         bathrooms=transaction_data.get("bathrooms", 1),
         surface_area=transaction_data.get("surface_area", 0.0),
         price_per_night=transaction_data["price_per_night"],
         currency=transaction_data.get("currency", "EUR"),
         amenities=transaction_data.get("amenities", []),
         description=transaction_data.get("description", ""),
         house_rules=transaction_data.get("house_rules", []),
         latitude=transaction_data.get("latitude"),
         longitude=transaction_data.get("longitude"),
         certification_status="validated",
         created_at=datetime.fromisoformat(transaction_data.get("created_at", datetime.now().isoformat()))
      )
   
   def to_dict(self) -> Dict[str, Any]:
      """Convertit en dictionnaire pour sérialisation JSON"""
      return {
         "property_id": self.property_id,
         "owner_wallet": self.owner_wallet,
         "title": self.title,
         "address": self.address,
         "city": self.city,
         "country": self.country,
         "postal_code": self.postal_code,
         "property_type": self.property_type,
         "max_occupancy": self.max_occupancy,
         "bedrooms": self.bedrooms,
         "bathrooms": self.bathrooms,
         "surface_area": self.surface_area,
         "price_per_night": self.price_per_night,
         "currency": self.currency,
         "amenities": self.amenities,
         "description": self.description,
         "house_rules": self.house_rules,
         "latitude": self.latitude,
         "longitude": self.longitude,
         "certification_status": self.certification_status,
         "certified_by": self.certified_by,
         "certification_date": self.certification_date.isoformat() if self.certification_date else None,
         "expiry_date": self.expiry_date.isoformat() if self.expiry_date else None,
         "created_at": self.created_at.isoformat(),
         "updated_at": self.updated_at.isoformat()
      }
   
   def update_certification(self, validator_public_key: str, expiry_months: int = 12):
      """Updates certification status"""
      self.certification_status = "validated"
      self.certified_by = validator_public_key
      self.certification_date = datetime.now()
      self.expiry_date = datetime.now().replace(month=datetime.now().month + expiry_months)
      self.updated_at = datetime.now()
   
   def revoke_certification(self, reason: str = ""):
      """Révoque la certification"""
      self.certification_status = "revoked"
      self.updated_at = datetime.now()
   
   def is_certified(self) -> bool:
      """Vérifie si le logement est actuellement certifié"""
      return (self.certification_status == "validated" and 
         self.expiry_date and 
         datetime.now() < self.expiry_date)
   
   def get_location_string(self) -> str:
      """Retourne l'adresse complète formatée"""
      return f"{self.address}, {self.city}, {self.postal_code}, {self.country}"
   
   def get_amenities_string(self) -> str:
      """Retourne les équipements sous forme de chaîne"""
      return ", ".join(self.amenities) if self.amenities else "Aucun équipement spécifié"
   
   def __str__(self) -> str:
      """Représentation textuelle du logement"""
      return f"Logement {self.property_id}: {self.title} à {self.city} ({self.certification_status})"
   
   def __repr__(self) -> str:
      """Représentation de débogage"""
      return f"Logement(id={self.property_id}, city={self.city}, status={self.certification_status})"