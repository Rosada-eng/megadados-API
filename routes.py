from fastapi import FastAPI, Query, Body, status, Response
from pydantic import BaseModel, Field


app = FastAPI()

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

inventory = {
    '1': Item(id=1, name='Camiseta do Palmeiras', description='camiseta verde versão de 2014', price=1.0, quantity=5), 
    '2': Item(id=2, name='Bermuda do Palmeiras', description='bermuda branca versão 2014', price=2.0, quantity=10), 
    '3': Item(id=3, name='Meia do Palmeiras', description='meia verde versão 2014', price=3.0, quantity=25)
    }

@app.get("/inventory/", 
        status_code=status.HTTP_200_OK,
        description="Retorna os produtos do inventário, coforme especificações de filtro.", )
def get_inventory(
    name: str = Query(
        default=None, 
        max_length=50, 
        title='Nome do Produto', 
        description='Informe o nome do produto desejado',
        examples={
            "default": {
                "value": None
            },
             "by name": {
                "summary": "Busca por nome",
                "description": "Busca pelo nome 'Camiseta do Palmeiras'",
                "value": "Camiseta do Palmeiras"
            },
        }),
    min_amount: int = Query(
        default=None, 
        ge=0, 
        title='Quantidade Mínima', 
        description='Informe a quantidade mínima em estoque',
        examples={
            "default": {
                "value": None
            },
             "by name": {
                "summary": "Adiciona quantidade mínima ao filtro",
                "description": "Limita a quantidade mínima do estoque em 1",
                "value": 10
            },
        }),
    max_amount: int = Query(
        default=None, 
        ge=0, 
        title='Quantidade Máxima', 
        description='Informe a quantidade máxima em estoque',
        examples={
            "default": {
                "value": None
            },
             "by name": {
                "summary": "Adiciona quantidade máxima ao filtro",
                "description": "Limita a quantidade máxima do estoque em 15",
                "value": 15
            },
        }),
    min_price: float = Query(
        default=None, 
        gt=0, 
        title='Preço Mínimo', 
        description='Informe o preço mínimo do produto desejado',
        examples={
            "default": {
                "value": None
            },
            "by price range": {
                "summary": "Adiciona limitador mínimo de preço",
                "description": "Limita o preço em 2.0 unidade",
                "value": 2.0 
            },
        }),
    max_price: float = Query(
        default=None, 
        gt=0, 
         title='Preço Máximo', 
         description='Informe o preço máximo do produto desejado',
         examples={
            "default": {
                "value": None
            },
            "by price range": {
                "summary": "Adiciona limitador máximo de preço",
                "description": "Limita o preço em 5.0 unidades",
                "value": 5.0 
            },
        }),
    contains: str = Query(
        default=None, 
        max_length=50, 
        title='Contém na descrição', 
        description='Informe uma palavra que a descrição deve conter',
        examples={
            "default": {
                "value": None
            },
            "by description": {
                "summary": "Busca pela cor verde",
                "description": "Busca por produtos que contém a cor verde na descrição",
                "value": "verde" 
            },
        }),
    
    ):

    filtered_inventory = inventory.copy()
    filtered_inventory = {k: v for k, v in filtered_inventory.items() if v.name == name} if name else filtered_inventory
    filtered_inventory = {k: v for k, v in filtered_inventory.items() if v.quantity >= min_amount} if min_amount else filtered_inventory
    filtered_inventory = {k: v for k, v in filtered_inventory.items() if v.quantity <= max_amount} if max_amount else filtered_inventory
    filtered_inventory = {k: v for k, v in filtered_inventory.items() if v.price >= min_price} if min_price else filtered_inventory
    filtered_inventory = {k: v for k, v in filtered_inventory.items() if v.price <= max_price} if max_price else filtered_inventory
    filtered_inventory = {k: v for k, v in filtered_inventory.items() if contains in v.description} if contains else filtered_inventory

    return filtered_inventory
    
@app.get("/inventory/{item_id}", 
    description="Retorna um item específico do inventário", )
def get_inventory(item_id: str, response: Response):

    filtered_inventory = inventory.get(item_id)
    if filtered_inventory:
        response.status_code = status.HTTP_200_OK
        return filtered_inventory
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": f"Item with id {item_id} not found"}

@app.post("/inventory/",
    description="Adiciona um item ao inventário")
def create_inventory(
    response: Response,
    item: Item = Body(
    embed=False,  
    description='Informe os dados do item a ser criado',
    examples={
        "normal": {
            "summary": "Exemplo de inserção normal",
            "description": "Cria um novo item sem informar o id",
            "value": {
                "name": "foo",
                "description": "bar",
                "price": 1.26,
                "quantity": 2
            }
        },
        "with_id": {
            "summary": "Exemplo de inserção com id válido",
            "description": "Cria um novo item informando um id válido",
            "value": {
                "id": "123456789",
                "name": "foo",
                "description": "bar",
                "price": 1.26,
                "quantity": 3
            }
        },
        "with_invalid_id": {
            "summary": "Exemplo de inserção com id inválido",
            "description": "NÃO cria um novo item informando, pois o id informado já existente",
            "value": {
                "id": "1",
                "name": "foo",
                "description": "bar",
                "price": 1.26,
                "quantity": 4
            }
        }
    }   
    ),
    ):

    if item.id:
        if inventory.get(item.id):
            response.status_code = status.HTTP_409_CONFLICT
            return {"error": f"Item with id {item.id} already exists"}
        else:
            inventory[item.id] = item
            response.status_code = status.HTTP_201_CREATED            
            return {"message": "Item created successfully", "item": item}
    else:
        item.id = str(len(inventory) + 1)
        inventory[item.id] = item
        response.status_code = status.HTTP_201_CREATED
        return {"message": "Item created successfully", "item": item}

@app.patch("/inventory/{item_id}",
    description="Atualiza dados de um item específico do inventário", 
    )
def update_inventory_item(
    item_id: str, 
    response: Response,
    name: str = Body(default=None), 
    description: str = Body(default=None), 
    price: float = Body(default=None), 
    quantity: int = Body(default=None),
    ):
    stored_item = inventory.get(item_id)
    if stored_item:
        stored_item.name = name if name else stored_item.name
        stored_item.description = description if description else stored_item.description
        stored_item.price = price if price else stored_item.price
        stored_item.quantity = quantity if quantity else stored_item.quantity
        inventory[item_id] = stored_item

        response.status_code = status.HTTP_200_OK
        return inventory

    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": f"Item with id {item_id} not found"}

@app.delete("/inventory/{item_id}",
    description="Remove um item específico do inventário")
def remove_inventory_item(item_id: str, response: Response):
    stored_item = inventory.get(item_id)
    if stored_item:
        del inventory[item_id]
        response.status_code = status.HTTP_200_OK
        return {"message": f"Item {item_id} successfully removed"}

    else:
        
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": f"Item with id {item_id} not found"}