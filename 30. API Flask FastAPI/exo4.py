from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, Field
from typing import List
from uuid import UUID, uuid4
import uvicorn

app = FastAPI(
    title="Exercice 4 - Commande",
    version="1.0.0"
)


from typing import List
from uuid import UUID, uuid4
from pydantic import BaseModel, Field, EmailStr, model_validator


class ItemModel(BaseModel):
    product_id: int
    quantity: int = Field(..., ge=1)
    price: float = Field(..., gt=0)

class Order(BaseModel):
    order_id: UUID = Field(default_factory=uuid4)
    customer_email: EmailStr
    items: List[ItemModel] = Field(..., min_length=1)
    total: float = 0.0

    @model_validator(mode='after')
    def calculer_total(self) -> 'Order':
        self.total = sum(item.price * item.quantity for item in self.items)
        return self


@app.post("/orders")
def create_order(order: Order):
    return {
        "message": "Order validated",
        "data": order
    }


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)