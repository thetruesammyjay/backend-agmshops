"""
AGM Store Builder - Dashboard Customer Endpoints

Aggregates unique customers from orders for the dashboard customer list.
"""

from typing import Optional
from fastapi import APIRouter, Query
from sqlalchemy import select, func, desc

from app.api.deps import DatabaseSession, CurrentUserId
from app.models.order import Order
from app.models.store import Store

router = APIRouter()


@router.get("/customers")
async def get_customers(
    user_id: CurrentUserId,
    db: DatabaseSession,
    store_id: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=100),
):
    """
    Get aggregated customer list from orders.

    Returns unique customers with total orders, total spent, and last order date.
    """
    # Base query: only orders belonging to the user's stores
    store_filter = select(Store.id).where(
        Store.user_id == user_id,
        Store.deleted_at.is_(None),
    )

    if store_id:
        store_filter = store_filter.where(Store.id == store_id)

    store_ids_subq = store_filter.scalar_subquery()

    # Aggregate customers by phone (unique identifier)
    query = (
        select(
            Order.customer_phone.label("phone"),
            Order.customer_name.label("name"),
            Order.customer_email.label("email"),
            func.count(Order.id).label("totalOrders"),
            func.sum(Order.total).label("totalSpent"),
            func.max(Order.created_at).label("lastOrderDate"),
        )
        .where(
            Order.store_id.in_(select(Store.id).where(
                Store.user_id == user_id,
                Store.deleted_at.is_(None),
                *([Store.id == store_id] if store_id else []),
            )),
            Order.deleted_at.is_(None),
        )
        .group_by(Order.customer_phone, Order.customer_name, Order.customer_email)
        .order_by(desc("lastOrderDate"))
    )

    # Count total customers
    count_query = (
        select(func.count(func.distinct(Order.customer_phone)))
        .where(
            Order.store_id.in_(select(Store.id).where(
                Store.user_id == user_id,
                Store.deleted_at.is_(None),
                *([Store.id == store_id] if store_id else []),
            )),
            Order.deleted_at.is_(None),
        )
    )
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0

    # Paginate
    offset = (page - 1) * limit
    query = query.offset(offset).limit(limit)

    result = await db.execute(query)
    rows = result.all()

    customers = []
    for i, row in enumerate(rows):
        customers.append({
            "id": f"cust_{offset + i + 1}",
            "name": row.name or "Unknown",
            "email": row.email or "",
            "phone": row.phone or "",
            "totalOrders": row.totalOrders or 0,
            "totalSpent": float(row.totalSpent or 0),
            "lastOrderDate": row.lastOrderDate.isoformat() if row.lastOrderDate else "",
        })

    return {
        "success": True,
        "data": customers,
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "pages": (total + limit - 1) // limit if total else 0,
        },
    }
