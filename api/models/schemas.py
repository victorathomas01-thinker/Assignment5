"""Request and response schemas for the sandwich maker API."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class SandwichBase(BaseModel):
    sandwich_name: str = Field(min_length=1, max_length=100)
    price: float = Field(ge=0, le=99.99)


class SandwichCreate(SandwichBase):
    pass


class SandwichUpdate(BaseModel):
    sandwich_name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    price: Optional[float] = Field(default=None, ge=0, le=99.99)


class Sandwich(SandwichBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class ResourceBase(BaseModel):
    item: str = Field(min_length=1, max_length=100)
    amount: int = Field(ge=0)


class ResourceCreate(ResourceBase):
    pass


class ResourceUpdate(BaseModel):
    item: Optional[str] = Field(default=None, min_length=1, max_length=100)
    amount: Optional[int] = Field(default=None, ge=0)


class Resource(ResourceBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class RecipeBase(BaseModel):
    amount: int = Field(ge=0)


class RecipeCreate(RecipeBase):
    sandwich_id: int
    resource_id: int


class RecipeUpdate(BaseModel):
    sandwich_id: Optional[int] = None
    resource_id: Optional[int] = None
    amount: Optional[int] = Field(default=None, ge=0)


class Recipe(RecipeBase):
    id: int
    sandwich_id: int
    resource_id: int
    sandwich: Optional[Sandwich] = None
    resource: Optional[Resource] = None
    model_config = ConfigDict(from_attributes=True)


class OrderDetailBase(BaseModel):
    amount: int = Field(ge=0)


class OrderDetailCreate(OrderDetailBase):
    order_id: int
    sandwich_id: int


class OrderDetailUpdate(BaseModel):
    order_id: Optional[int] = None
    sandwich_id: Optional[int] = None
    amount: Optional[int] = Field(default=None, ge=0)


class OrderDetail(OrderDetailBase):
    id: int
    order_id: int
    sandwich_id: int
    sandwich: Optional[Sandwich] = None
    model_config = ConfigDict(from_attributes=True)


class OrderBase(BaseModel):
    customer_name: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=300)


class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    customer_name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=300)


class Order(OrderBase):
    id: int
    order_date: Optional[datetime] = None
    order_details: list[OrderDetail] = Field(default_factory=list)
    model_config = ConfigDict(from_attributes=True)
