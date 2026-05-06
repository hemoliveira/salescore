from decimal import Decimal

from fastapi import APIRouter, HTTPException, status

from models.order import Order
from models.order_item import OrderItem
from repositories.order_repository import OrderRepository
from schemas.order_schema import OrderCreate, OrderResponse

router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
)

repo = OrderRepository()


@router.get("", response_model=list[OrderResponse])
def find_all_orders():
    orders = repo.find_all()
    return [order.to_dict() for order in orders]


@router.get("/{order_id}", response_model=OrderResponse)
def find_order_by_id(order_id: int):
    try:
        order = repo.find_by_id(order_id)

        if order is None:
            raise HTTPException(status_code=404, detail="Order not found")

        return order.to_dict()

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("", status_code=status.HTTP_201_CREATED)
def create_order(payload: OrderCreate):
    try:
        order = Order(
            customer_id=payload.customer_id,
            order_date=payload.order_date,
        )

        for item_data in payload.items:
            item = OrderItem(
                product_id=item_data.product_id,
                quantity=item_data.quantity,
                unit_price=Decimal("0"),
            )
            order.add_item(item)

        new_id = repo.create(order)

        return {
            "message": "Order created successfully",
            "order_id": new_id,
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{order_id}")
def delete_order(order_id: int):
    try:
        deleted = repo.delete(order_id)

        if not deleted:
            raise HTTPException(status_code=404, detail="Order not found")

        return {"message": "Order deleted successfully"}

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
