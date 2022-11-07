from fastapi import Depends, FastAPI, HTTPException, Query, Body, status, Response
from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#! PRODUCTS
@app.get("/products/", response_model=list[schemas.Product])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = crud.get_all_products(db, skip=skip, limit=limit)
    return products

@app.get("/products/{product_id}", response_model=schemas.Product)
def read_product(product_id: int, db: Session = Depends(get_db)):
    db_product = crud.get_product_by_id(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@app.post("/products/", response_model=schemas.Product)
def create_product(product: schemas.ProductBase, db: Session = Depends(get_db)):
    db_product = crud.get_product_by_name(db, name=product.name)
    if db_product:
        raise HTTPException(status_code=400, detail="Product already registered")
    return crud.create_product(db=db, Product=product)

@app.put("/products/{product_id}", response_model=schemas.Product)
def update_product(product_id: int, product: schemas.ProductBase, db: Session = Depends(get_db)):
    db_product = crud.get_product_by_id(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    db_product.name = product.name
    db_product.description = product.description
    db_product.price = product.price
    db.commit()
    return db_product


@app.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = crud.get_product_by_id(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(db_product)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


#! TRANSACTIONS
@app.get("/products/{product_id}/transactions", response_model=list[schemas.Transaction])
def read_transactions(product_id: int, db: Session = Depends(get_db)):
    db_product = crud.get_product_by_id(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product.transactions

@app.post("/products/{product_id}/transactions", response_model=schemas.Transaction)
def create_transaction(product_id: int, transaction: schemas.TransactionBase, db: Session = Depends(get_db)):
    db_product = crud.get_product_by_id(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    if transaction.type == "remove" and db_product.amount < transaction.amount:
        raise HTTPException(status_code=400, detail="Not enough products in stock")
    else:
        db_transaction = crud.create_transaction(db=db, transaction=transaction, product_id=product_id)
        db.add(db_transaction)
        if transaction.type == "add":
            db_product.amount += transaction.amount
        elif transaction.type == "remove":
            db_product.amount -= transaction.amount
        db.commit()
        db.refresh(db_transaction)
        return db_transaction

@app.put("/products/{product_id}/transactions/{transaction_id}", response_model=schemas.Transaction)
def update_transaction(product_id: int, transaction_id: int, transaction: schemas.TransactionBase, db: Session = Depends(get_db)):
    db_product = crud.get_product_by_id(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    db_transaction = crud.get_transaction_by_id(db, transaction_id=transaction_id)
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")

    if transaction.type == "remove" and db_product.amount < transaction.amount:
        raise HTTPException(status_code=400, detail="Not enough products in stock")
    else:
        db_transaction.type = transaction.type
        db_transaction.amount = transaction.amount
        db_product.amount += transaction.amount
        db.commit()
        return db_transaction
@app.delete("/products/{product_id}/transactions/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction(product_id: int, transaction_id: int, db: Session = Depends(get_db)):
    db_product = crud.get_product_by_id(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    db_transaction = crud.get_transaction_by_id(db, transaction_id=transaction_id)
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    db.delete(db_transaction)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

