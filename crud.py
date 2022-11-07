from sqlalchemy.orm import Session

import models, schemas

def get_product_by_id(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def get_product_by_name(db: Session, name: str):
    return db.query(models.Product).filter(models.Product.name == name).first()

def get_all_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Product).offset(skip).limit(limit).all()

def create_product(db: Session, Product: schemas.Product):
    db_Product = models.Product(**Product.dict())
    db.add(db_Product)
    db.commit()
    db.refresh(db_Product)
    return db_Product

def update_product(db: Session, product_id: int, Product: schemas.Product):
    db_Product = get_product_by_id(db, product_id=product_id)
    db_Product.name = Product.name
    db_Product.description = Product.description
    db_Product.price = Product.price
    db_Product.amount = Product.amount
    db.commit()
    return db_Product

def delete_product(db: Session, product_id: int):
    db_Product = get_product_by_id(db, product_id=product_id)
    db.delete(db_Product)
    db.commit()
    return db_Product

def get_transactions_by_product_id(db: Session, product_id: int):
    return db.query(models.Transaction).filter(models.Transaction.product_id == product_id).all()

def get_transaction_by_id(db: Session, transaction_id: int):
    return db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()
    
def create_transaction(db: Session, transaction: schemas.Transaction, product_id: int):
    db_transaction = models.Transaction(**transaction.dict(), product_id=product_id)
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

def delete_transaction(db: Session, transaction_id: int):
    db_transaction = db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()
    db.delete(db_transaction)
    db.commit()
    return db_transaction


