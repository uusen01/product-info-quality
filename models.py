#This file handles all the models in our database. Helps establishes schema and internal relationships
from sqlalchemy import Column, Numeric, ForeignKey, Integer, String, Boolean, DateTime, Text
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
import json

DBModelBase = declarative_base()


class Product(DBModelBase):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    attributes = Column(Text, nullable=True)
    information_score = Column(Integer, nullable=False, default=0)
    barcode = Column(Numeric, nullable=False, default=0)
    price = Column(String(255), nullable=False, default=0)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def set_attributes(self, data: dict):
        self.attributes = json.dumps(data)

    def get_attributes(self) -> dict:
        if not self.attributes:
            return {}
        return json.loads(self.attributes)