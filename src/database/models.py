"""
Database models for Pizza Calculator application.
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any
from datetime import datetime
from decimal import Decimal

@dataclass
class PizzaStyle:
    """Pizza style model."""
    id: Optional[int] = None
    name: str = ""
    description: Optional[str] = None
    typical_hydration: Decimal = Decimal('65.00')
    typical_salt_percentage: Decimal = Decimal('2.00')
    typical_yeast_percentage: Decimal = Decimal('0.25')
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

@dataclass
class PrefermentMethod:
    """Preferment method model."""
    id: Optional[int] = None
    name: str = ""
    description: Optional[str] = None
    typical_percentage: Decimal = Decimal('20.00')
    fermentation_time_hours: int = 12
    temperature_celsius: int = 20
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

@dataclass
class Recipe:
    """Recipe model."""
    id: Optional[int] = None
    name: str = ""
    pizza_style_id: int = 0
    preferment_method_id: Optional[int] = None
    flour_weight: Decimal = Decimal('1000.00')
    water_percentage: Decimal = Decimal('65.00')
    salt_percentage: Decimal = Decimal('2.00')
    yeast_percentage: Decimal = Decimal('0.25')
    preferment_percentage: Decimal = Decimal('0.00')
    oil_percentage: Decimal = Decimal('0.00')
    sugar_percentage: Decimal = Decimal('0.00')
    fermentation_time_hours: int = 24
    fermentation_temperature: int = 20
    notes: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

@dataclass
class Calculation:
    """Calculation model."""
    id: Optional[int] = None
    recipe_id: int = 0
    number_of_pizzas: int = 4
    pizza_weight: Decimal = Decimal('250.00')
    total_flour: Decimal = Decimal('0.00')
    total_water: Decimal = Decimal('0.00')
    total_salt: Decimal = Decimal('0.00')
    total_yeast: Decimal = Decimal('0.00')
    total_oil: Decimal = Decimal('0.00')
    total_sugar: Decimal = Decimal('0.00')
    preferment_flour: Decimal = Decimal('0.00')
    preferment_water: Decimal = Decimal('0.00')
    preferment_yeast: Decimal = Decimal('0.00')
    main_dough_flour: Decimal = Decimal('0.00')
    main_dough_water: Decimal = Decimal('0.00')
    main_dough_salt: Decimal = Decimal('0.00')
    main_dough_yeast: Decimal = Decimal('0.00')
    calculated_at: Optional[datetime] = None

@dataclass
class Widget:
    """Widget model."""
    id: Optional[int] = None
    name: str = ""
    widget_type: str = "calculator"
    configuration: Optional[Dict[str, Any]] = None
    is_active: bool = True
    display_order: int = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None