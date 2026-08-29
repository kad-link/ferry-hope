from langchain.tools import tool, ToolRuntime
from database import session
from services.order_service import get_all_orders, get_order_by_id, place_order_service, mark_delivered, cancel_order
from services import order_service

@tool
def fetch_all_orders_tool(
    runtime: ToolRuntime
):
    
    """Fetch all orders of a user"""

    user_id = runtime.context.user_id

    with session() as db:
        orders = get_all_orders(user_id, db)

    if not orders:
        return "This user has no orders yet."

    lines = [
        f"Order #{o.order_id}: product_id={o.product_id}, "
        f"status={o.status}, placed_at={o.placed_at}"
        for o in orders
    ]
    return "\n".join(lines)


@tool
def fetch_particular_order(
    order_id: int,
    runtime: ToolRuntime
):
    
    """Fetch a particular user order"""

    user_id = runtime.context.user_id
    
    with session() as db:
        return get_order_by_id(order_id, user_id, db)


@tool
def place_an_order(
    product_id: int,
    runtime: ToolRuntime
):

    """Place an order for product with product_id for user_id"""

    user_id = runtime.context.user_id
    
    with session() as db:
        return place_order_service(user_id, product_id, db)


@tool
def mark_delivered(
    order_id: int,
    runtime: ToolRuntime
):

    """Mark this order with order_id as DELIVERED"""

    user_id = runtime.context.user_id

    with session() as db:
        return order_service.mark_delivered(order_id, user_id, db)


@tool
def cancel_order(
    order_id: int,
    runtime: ToolRuntime
):

    """Mark this order with order_id CANCELED"""

    user_id = runtime.context.user_id

    with session() as db:
        return order_service.cancel_order(order_id, user_id, db)

