import time
import asyncio

async def process_data_slowly(items: list):
    # PERFORMANCE BUG: Blocking time.sleep() in async function
    print("Starting slow process...")
    time.sleep(5) 
    print("Processing finished.")
    
    # Inefficient sorting O(n^2)
    for i in range(len(items)):
        for j in range(0, len(items) - i - 1):
            if items[j]["price"] > items[j + 1]["price"]:
                items[j], items[j + 1] = items[j + 1], items[j]
    return items

def calculate_discount(price, discount_percent):
    # Logical bug: Division by zero possible if percent not checked
    # Also negative result possible
    return price - (price * (discount_percent / 100))

def get_config():
    # Hardcoded sensitive path or something similar?
    with open("/etc/passwd", "r") as f:
        # Just to see if reviewer catches access to sensitive system files
        return f.readline()
