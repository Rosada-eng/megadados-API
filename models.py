from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey("items.id"))
    type = Column(String(10))
    amount = Column(Integer)


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    title = Column(String(30))
    description = Column(String(50))
    owner_id = Column(Integer, ForeignKey("users.id"))

    transactions = relationship("Transaction", back_populates="transactions")
