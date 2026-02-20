"""
AGM Store Builder - Analytics Service

Business logic for dashboard analytics and reporting.
"""

from typing import Dict, Any, Optional, List
from datetime import datetime, timezone, timedelta
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.order import Order
from app.models.product import Product
from app.models.store import Store
from app.repositories.store_repository import StoreRepository
from app.repositories.order_repository import OrderRepository
from app.repositories.product_repository import ProductRepository


class AnalyticsService:
    """Analytics service for dashboard and reporting."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.store_repo = StoreRepository(db)
        self.order_repo = OrderRepository(db)
        self.product_repo = ProductRepository(db)
    
    def _get_date_range(
        self,
        period: str,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
    ) -> tuple:
        """Get date range for analytics period."""
        now = datetime.now(timezone.utc)
        
        if period == "today":
            start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            end = now
        elif period == "week":
            start = now - timedelta(days=7)
            end = now
        elif period == "month":
            start = now - timedelta(days=30)
            end = now
        elif period == "year":
            start = now - timedelta(days=365)
            end = now
        elif period == "custom" and date_from and date_to:
            start = datetime.fromisoformat(date_from)
            end = datetime.fromisoformat(date_to)
        else:
            start = now - timedelta(days=30)
            end = now
        
        return start, end
    
    async def get_dashboard_analytics(
        self,
        user_id: str,
        store_id: Optional[str] = None,
        period: str = "month",
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Get dashboard overview analytics."""
        start_date, end_date = self._get_date_range(period, date_from, date_to)
        
        # Get user's stores
        stores = await self.store_repo.get_by_user_id(user_id)
        store_ids = [s.id for s in stores]
        
        if store_id:
            store_ids = [store_id] if store_id in store_ids else []
        
        if not store_ids:
            return self._empty_dashboard()
        
        # Overview stats
        overview = await self._get_overview_stats(store_ids, start_date, end_date)
        
        # Recent orders
        recent_orders = await self._get_recent_orders(store_ids, limit=5)
        
        # Top products
        top_products = await self._get_top_products(store_ids, start_date, end_date, limit=5)
        
        # Store summaries
        store_summaries = await self._get_store_summaries(stores, start_date, end_date)
        
        return {
            "overview": overview,
            "recentOrders": recent_orders,
            "topProducts": top_products,
            "stores": store_summaries,
        }
    
    async def _get_overview_stats(
        self,
        store_ids: List[str],
        start_date: datetime,
        end_date: datetime,
    ) -> Dict[str, Any]:
        """Get overview statistics."""
        # Revenue and order counts
        order_stats = await self.db.execute(
            select(
                func.coalesce(func.sum(Order.total), 0).label("total_revenue"),
                func.count(Order.id).label("total_orders"),
                func.sum(func.if_(Order.status == 'pending', 1, 0)).label("pending_orders"),
                func.sum(func.if_(Order.status.in_(['delivered', 'fulfilled']), 1, 0)).label("completed_orders"),
            ).where(
                Order.store_id.in_(store_ids),
                Order.payment_status == 'paid',
                Order.created_at >= start_date,
                Order.created_at <= end_date,
                Order.deleted_at.is_(None),
            )
        )
        row = order_stats.one()
        
        # Product counts
        product_stats = await self.db.execute(
            select(
                func.count(Product.id).label("total_products"),
                func.sum(func.if_(Product.is_active == True, 1, 0)).label("active_products"),
            ).where(
                Product.store_id.in_(store_ids),
                Product.deleted_at.is_(None),
            )
        )
        product_row = product_stats.one()
        
        return {
            "totalRevenue": float(row.total_revenue or 0),
            "totalOrders": row.total_orders or 0,
            "pendingOrders": row.pending_orders or 0,
            "completedOrders": row.completed_orders or 0,
            "totalProducts": product_row.total_products or 0,
            "activeProducts": product_row.active_products or 0,
            "totalStores": len(store_ids),
        }
    
    async def _get_recent_orders(
        self,
        store_ids: List[str],
        limit: int = 5,
    ) -> List[Dict[str, Any]]:
        """Get recent orders."""
        result = await self.db.execute(
            select(Order).where(
                Order.store_id.in_(store_ids),
                Order.deleted_at.is_(None),
            ).order_by(Order.created_at.desc()).limit(limit)
        )
        orders = result.scalars().all()
        
        return [
            {
                "id": order.id,
                "order_number": order.order_number,
                "customer_name": order.customer_name,
                "total": float(order.total),
                "status": order.status,
                "created_at": str(order.created_at),
            }
            for order in orders
        ]
    
    async def _get_top_products(
        self,
        store_ids: List[str],
        start_date: datetime,
        end_date: datetime,
        limit: int = 5,
    ) -> List[Dict[str, Any]]:
        """Get top selling products."""
        # This is a simplified version - actual implementation would join with order_items
        result = await self.db.execute(
            select(Product).where(
                Product.store_id.in_(store_ids),
                Product.is_active == True,
                Product.deleted_at.is_(None),
            ).order_by(Product.view_count.desc()).limit(limit)
        )
        products = result.scalars().all()
        
        return [
            {
                "id": product.id,
                "name": product.name,
                "sales_count": 0,  # Would be calculated from order_items
                "revenue": 0,
            }
            for product in products
        ]
    
    async def _get_store_summaries(
        self,
        stores: List[Store],
        start_date: datetime,
        end_date: datetime,
    ) -> List[Dict[str, Any]]:
        """Get store summaries with stats."""
        summaries = []
        
        for store in stores:
            product_count = await self.db.execute(
                select(func.count(Product.id)).where(
                    Product.store_id == store.id,
                    Product.deleted_at.is_(None),
                )
            )
            
            order_stats = await self.db.execute(
                select(
                    func.count(Order.id),
                    func.coalesce(func.sum(Order.total), 0),
                ).where(
                    Order.store_id == store.id,
                    Order.payment_status == 'paid',
                    Order.created_at >= start_date,
                    Order.created_at <= end_date,
                    Order.deleted_at.is_(None),
                )
            )
            order_row = order_stats.one()
            
            summaries.append({
                "id": store.id,
                "name": store.display_name,
                "username": store.username,
                "product_count": product_count.scalar() or 0,
                "order_count": order_row[0] or 0,
                "revenue": float(order_row[1] or 0),
            })
        
        return summaries
    
    def _empty_dashboard(self) -> Dict[str, Any]:
        """Return empty dashboard data."""
        return {
            "overview": {
                "totalRevenue": 0,
                "totalOrders": 0,
                "pendingOrders": 0,
                "completedOrders": 0,
                "totalProducts": 0,
                "activeProducts": 0,
                "totalStores": 0,
            },
            "recentOrders": [],
            "topProducts": [],
            "stores": [],
        }
    
    async def get_revenue_stats(
        self,
        user_id: str,
        store_id: Optional[str] = None,
        period: str = "month",
        group_by: str = "day",
    ) -> Dict[str, Any]:
        """Get revenue statistics with chart data."""
        start_date, end_date = self._get_date_range(period)
        stores = await self.store_repo.get_by_user_id(user_id)
        store_ids = [s.id for s in stores]
        
        if store_id:
            store_ids = [store_id] if store_id in store_ids else []
        
        if not store_ids:
            return {"total": 0, "paid": 0, "pending": 0, "chartData": []}
        
        # Get totals
        result = await self.db.execute(
            select(
                func.coalesce(func.sum(Order.total), 0).label("total"),
                func.sum(func.if_(Order.payment_status == 'paid', Order.total, 0)).label("paid"),
                func.sum(func.if_(Order.payment_status == 'pending', Order.total, 0)).label("pending"),
            ).where(
                Order.store_id.in_(store_ids),
                Order.created_at >= start_date,
                Order.created_at <= end_date,
                Order.deleted_at.is_(None),
            )
        )
        row = result.one()
        
        return {
            "total": float(row.total or 0),
            "paid": float(row.paid or 0),
            "pending": float(row.pending or 0),
            "thisMonth": float(row.paid or 0),
            "lastMonth": 0,
            "growth": 0,
            "chartData": [],
        }
    
    async def get_order_stats(
        self,
        user_id: str,
        store_id: Optional[str] = None,
        period: str = "month",
    ) -> Dict[str, Any]:
        """Get order statistics."""
        start_date, end_date = self._get_date_range(period)
        stores = await self.store_repo.get_by_user_id(user_id)
        store_ids = [s.id for s in stores]
        
        if store_id:
            store_ids = [store_id] if store_id in store_ids else []
        
        if not store_ids:
            return {"total": 0, "averageOrderValue": 0, "chartData": []}
        
        result = await self.db.execute(
            select(
                func.count(Order.id).label("total"),
                func.avg(Order.total).label("average"),
            ).where(
                Order.store_id.in_(store_ids),
                Order.created_at >= start_date,
                Order.created_at <= end_date,
                Order.deleted_at.is_(None),
            )
        )
        row = result.one()
        
        return {
            "total": row.total or 0,
            "pending": 0,
            "confirmed": 0,
            "processing": 0,
            "shipped": 0,
            "delivered": 0,
            "cancelled": 0,
            "averageOrderValue": float(row.average or 0),
            "chartData": [],
        }
    
    async def get_product_performance(
        self,
        user_id: str,
        store_id: Optional[str] = None,
        period: str = "month",
        limit: int = 10,
    ) -> Dict[str, Any]:
        """Get product performance analytics."""
        stores = await self.store_repo.get_by_user_id(user_id)
        store_ids = [s.id for s in stores]
        
        if store_id:
            store_ids = [store_id] if store_id in store_ids else []
        
        if not store_ids:
            return {"totalProducts": 0, "activeProducts": 0, "topSelling": []}
        
        result = await self.db.execute(
            select(
                func.count(Product.id).label("total"),
                func.sum(func.if_(Product.is_active == True, 1, 0)).label("active"),
                func.sum(func.if_(Product.stock_quantity == 0, 1, 0)).label("out_of_stock"),
                func.sum(func.if_(Product.stock_quantity <= Product.low_stock_threshold, 1, 0)).label("low_stock"),
            ).where(
                Product.store_id.in_(store_ids),
                Product.deleted_at.is_(None),
            )
        )
        row = result.one()
        
        return {
            "totalProducts": row.total or 0,
            "activeProducts": row.active or 0,
            "outOfStock": row.out_of_stock or 0,
            "lowStock": row.low_stock or 0,
            "topSelling": [],
            "recentlyAdded": [],
        }
    
    async def get_customer_analytics(
        self,
        user_id: str,
        store_id: Optional[str] = None,
        period: str = "month",
    ) -> Dict[str, Any]:
        """Get customer analytics."""
        start_date, end_date = self._get_date_range(period)
        stores = await self.store_repo.get_by_user_id(user_id)
        store_ids = [s.id for s in stores]
        
        if store_id:
            store_ids = [store_id] if store_id in store_ids else []
        
        if not store_ids:
            return {"totalCustomers": 0, "newCustomers": 0, "topCustomers": []}
        
        # Count unique customers by phone/email
        result = await self.db.execute(
            select(
                func.count(func.distinct(Order.customer_phone)).label("total"),
            ).where(
                Order.store_id.in_(store_ids),
                Order.created_at >= start_date,
                Order.created_at <= end_date,
                Order.deleted_at.is_(None),
            )
        )
        row = result.one()
        
        return {
            "totalCustomers": row.total or 0,
            "newCustomers": 0,
            "returningCustomers": 0,
            "topCustomers": [],
        }
