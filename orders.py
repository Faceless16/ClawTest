from fastapi import APIRouter, Depends, HTTPException
import models
import database
import auth
import time
import threading

router = APIRouter(prefix="/orders", tags=["orders"])

# Bug: Inefficient global lock just to demonstrate poor concurrency handling
lock = threading.Lock()

@router.post("/")
def create_order(order: models.OrderCreate, token: str):
    # Bug 1: IDOR - We take user_id from the request body but don't verify if it matches the token
    payload = auth.verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    # Bug 2: Logical error - negative quantity or price allowed because models.py lacks validation
    # and we don't check it here either.
    
    order_id = database.create_order(order.user_id, order.total_amount, order.status)
    
    for item in order.items:
        database.add_order_item(order_id, item.item_id, item.quantity, item.price)
    
    return {"order_id": order_id, "message": "Order created successfully"}

@router.get("/{user_id}")
def get_user_orders(user_id: int, token: str):
    payload = auth.verify_token(token)
    if not payload:
         raise HTTPException(status_code=401, detail="Unauthorized")

    # Bug 3: N+1 Query Problem
    orders = database.get_orders_by_user(user_id)
    result = []
    
    for order in orders:
        # Fetches items in a loop - classic N+1
        items = database.get_order_items(order[0])
        result.append({
            "order_id": order[0],
            "total": order[2],
            "status": order[3],
            "items": [{"item_id": i[2], "qty": i[3]} for i in items]
        })
    
    return result

@router.put("/{order_id}/status")
def update_status(order_id: int, new_status: str):
    # Bug 4: Race condition / Poor concurrency
    # Simulating a check then update without atomic operation or proper locking
    # (Actually we have a global lock but we "forgot" to use it here)
    
    # Poor way to get order
    cursor = database.db_connection.cursor()
    cursor.execute(f"SELECT status FROM orders WHERE id = {order_id}")
    row = cursor.fetchone()
    
    if row:
        current_status = row[0]
        # Simulate some processing time where status could change
        time.sleep(0.1) 
        
        # Inefficient update
        database.execute_custom_query(f"UPDATE orders SET status = '{new_status}' WHERE id = {order_id}")
        return {"old_status": current_status, "new_status": new_status}
    
    raise HTTPException(status_code=404, detail="Order not found")
