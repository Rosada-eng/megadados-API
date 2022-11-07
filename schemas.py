from pydantic import BaseModel, Field
"""
    Schemas for the API

"""

class Item(BaseModel):
    id: str = Field(
        default=None,
        description="Id único do produto. Não precisa ser informado."
        )
    name: str = Field(
        ...,
        title='Nome do Produto',
        description="(obrigatório) Nome do produto",
        min_length=3, 
        max_length=50
        )
    description: str  | None = Field(
        default=None, 
        title='Descrição do Produto', 
        description="Descreva as características do produto",
        max_length=50
    )   
    price: float = Field(
        ..., 
        title='Preço',
        description='(obrigatório) Preço do Produto. Deve ser maior que zero.', 
        gt=0, 
    )
    quantity: int = Field(
        default=1,
        ge=0,
        title='Quantidade',
        description='Quantidade do Produto em estoque. Deve ser maior ou igual a zero.'
        )

    class Config:
        orm_mode = True


class Transaction(BaseModel):
    id: str = Field(
        default=None,
        description="Id único da transação. Não precisa ser informado."
        )
    item_id: str = Field(
        ...,
        title='Id do Produto',
        description="(obrigatório) Id do produto",
        )
    type: str = Field(
        ...,
        title='Tipo da Transação (entrada ou saída)',
        description="(obrigatório) Tipo da transação (entrada ou saída)",
        regex=r'(add)|(remove)'
    )
    amount: int = Field(
        default=1,
        gt=0,
        title='Quantidade',
        description='Quantidade do Produto em estoque. Deve ser maior que zero.'
        )

    class Config:
        orm_mode = True