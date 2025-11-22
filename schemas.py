"""
Database Schemas for LVFRD (Las Vegas Fire & Rescue Department)

Each Pydantic model represents a MongoDB collection. The collection name
is the lowercase of the class name. For example:
- Unit -> "unit"
- Member -> "member"
- ContactInfo -> "contactinfo"
"""

from pydantic import BaseModel, Field
from typing import Optional, List

class Unit(BaseModel):
    """
    Fire/Rescue operational unit
    Example: Engine 1, Truck 3, Rescue 5, Battalion 1
    """
    name: str = Field(..., description="Unit display name, e.g., 'Engine 1'")
    station: Optional[str] = Field(None, description="Assigned station, e.g., 'Station 1'")
    unit_type: str = Field(..., description="Type of unit: Engine, Truck, Rescue, Battalion, Squad, etc.")
    status: str = Field("Available", description="Current status: Available, On Scene, Out of Service, etc.")
    district: Optional[str] = Field(None, description="District or area of responsibility")

class Member(BaseModel):
    """
    Department member with role in the hierarchy
    """
    name: str = Field(..., description="Full name")
    rank: str = Field(..., description="Rank/Title e.g., Fire Chief, Deputy Chief, Captain, Engineer")
    division: Optional[str] = Field(None, description="Division/Bureau e.g., Operations, Prevention, Training")
    unit: Optional[str] = Field(None, description="Assigned unit or station, e.g., 'Engine 1' or 'Station 1'")
    phone: Optional[str] = Field(None, description="Contact phone")
    email: Optional[str] = Field(None, description="Contact email")

class ContactInfo(BaseModel):
    """
    General contact and public information for the department
    """
    department_name: str = Field("Las Vegas Fire & Rescue", description="Official department name")
    non_emergency: Optional[str] = Field(None, description="Non-emergency phone number")
    emergency: str = Field("911", description="Emergency number")
    address: Optional[str] = Field(None, description="Headquarters address")
    website: Optional[str] = Field(None, description="Official website URL")
    email: Optional[str] = Field(None, description="Public information email")
    social: Optional[List[str]] = Field(default=None, description="List of social links")
