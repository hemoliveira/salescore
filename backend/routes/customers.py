from fastapi import APIRouter, HTTPException, status

from models.customer import Customer
from repositories.customer_repository import CustomerRepository
from schemas.customer_schema import CustomerCreate, CustomerResponse, CustomerUpdate

router = APIRouter(
    prefix="/customers",
    tags=["Customers"],
)

repo = CustomerRepository()


@router.get("", response_model=list[CustomerResponse])
def find_all_customers():
    customers = repo.find_all()
    return [customer.to_dict() for customer in customers]


@router.get("/{customer_id}", response_model=CustomerResponse)
def find_customer_by_id(customer_id: int):
    customer = repo.find_by_id(customer_id)

    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")

    return customer.to_dict()


@router.post("", status_code=status.HTTP_201_CREATED)
def create_customer(payload: CustomerCreate):
    try:
        customer = Customer(
            name=payload.name,
            city=payload.city,
        )
        new_id = repo.create(customer)

        return {
            "message": "Customer created successfully",
            "customer_id": new_id,
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{customer_id}")
def update_customer(customer_id: int, payload: CustomerUpdate):
    existing = repo.find_by_id(customer_id)

    if existing is None:
        raise HTTPException(status_code=404, detail="Customer not found")

    try:
        customer = Customer(
            customer_id=customer_id,
            name=payload.name,
            city=payload.city,
        )

        updated = repo.update(customer)

        if not updated:
            raise HTTPException(status_code=404, detail="Customer not found")

        return {"message": "Customer updated successfully"}

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{customer_id}")
def delete_customer(customer_id: int):
    try:
        deleted = repo.delete(customer_id)

        if not deleted:
            raise HTTPException(status_code=404, detail="Customer not found")

        return {"message": "Customer deleted successfully"}

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
