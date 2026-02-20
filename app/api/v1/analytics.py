"""
AGM Store Builder - Analytics Endpoints

Analytics and reporting endpoints for dashboard data.
"""

from typing import Optional
from fastapi import APIRouter, Query

from app.api.deps import DatabaseSession, CurrentUserId
from app.services.analytics_service import AnalyticsService
from app.schemas.analytics import (
    DashboardResponse,
    RevenueResponse,
    OrderStatsResponse,
    ProductPerformanceResponse,
    CustomerAnalyticsResponse,
)

router = APIRouter()


@router.get("/dashboard", response_model=DashboardResponse)
async def get_dashboard(
    user_id: CurrentUserId,
    db: DatabaseSession,
    store_id: Optional[str] = None,
    period: str = Query("month", pattern="^(today|week|month|year|custom)$"),
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
):
    """
    Get dashboard analytics overview.
    
    Returns summary stats, recent orders, and top products.
    """
    analytics_service = AnalyticsService(db)
    result = await analytics_service.get_dashboard_analytics(
        user_id=user_id,
        store_id=store_id,
        period=period,
        date_from=date_from,
        date_to=date_to,
    )
    
    return {
        "success": True,
        "data": result,
    }


@router.get("/revenue", response_model=RevenueResponse)
async def get_revenue_stats(
    user_id: CurrentUserId,
    db: DatabaseSession,
    store_id: Optional[str] = None,
    period: str = Query("month", pattern="^(today|week|month|year)$"),
    group_by: str = Query("day", pattern="^(day|week|month)$"),
):
    """
    Get revenue statistics.
    
    Returns revenue data with chart data for visualization.
    """
    analytics_service = AnalyticsService(db)
    result = await analytics_service.get_revenue_stats(
        user_id=user_id,
        store_id=store_id,
        period=period,
        group_by=group_by,
    )
    
    return {
        "success": True,
        "data": result,
    }


@router.get("/orders", response_model=OrderStatsResponse)
async def get_order_stats(
    user_id: CurrentUserId,
    db: DatabaseSession,
    store_id: Optional[str] = None,
    period: str = Query("month", pattern="^(today|week|month|year)$"),
):
    """
    Get order statistics.
    
    Returns order counts by status and average order value.
    """
    analytics_service = AnalyticsService(db)
    result = await analytics_service.get_order_stats(
        user_id=user_id,
        store_id=store_id,
        period=period,
    )
    
    return {
        "success": True,
        "data": result,
    }


@router.get("/products", response_model=ProductPerformanceResponse)
async def get_product_performance(
    user_id: CurrentUserId,
    db: DatabaseSession,
    store_id: Optional[str] = None,
    period: str = Query("month", pattern="^(today|week|month|year)$"),
    limit: int = Query(10, ge=1, le=50),
):
    """
    Get product performance analytics.
    
    Returns top selling products and stock information.
    """
    analytics_service = AnalyticsService(db)
    result = await analytics_service.get_product_performance(
        user_id=user_id,
        store_id=store_id,
        period=period,
        limit=limit,
    )
    
    return {
        "success": True,
        "data": result,
    }


@router.get("/customers", response_model=CustomerAnalyticsResponse)
async def get_customer_analytics(
    user_id: CurrentUserId,
    db: DatabaseSession,
    store_id: Optional[str] = None,
    period: str = Query("month", pattern="^(today|week|month|year)$"),
):
    """
    Get customer analytics.
    
    Returns customer counts and top customers.
    """
    analytics_service = AnalyticsService(db)
    result = await analytics_service.get_customer_analytics(
        user_id=user_id,
        store_id=store_id,
        period=period,
    )
    
    return {
        "success": True,
        "data": result,
    }
