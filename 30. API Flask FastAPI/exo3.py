from enum import Enum
from typing import Optional

import uvicorn
from fastapi import FastAPI, status
from pydantic import BaseModel, EmailStr

app = FastAPI()


class Category(str, Enum):
    ELECTRONICS = "ELECTRONICS"
    CLOTHING = "CLOTHING"
    FOOD = "FOOD"
    OTHER = "OTHER"


class Supplier(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None


class Product(BaseModel):
    name: str
    price: float
    category: Category
    stock: int
    supplier: Supplier


@app.post("/products", status_code=status.HTTP_201_CREATED)
def create_product(product: Product):
    return {"message": "Product created successfully", "product": product}


if __name__ == "__main__":
    uvicorn.run("exo3:app", host="127.0.0.1", port=8002, reload=True)
