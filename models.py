from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("items.id"))
    type = Column(String(10))
    amount = Column(Integer)


class Product(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    description = Column(String(50))
    price = Column(Float)
    amount = Column(Integer)

    transactions = relationship("Transaction", )
