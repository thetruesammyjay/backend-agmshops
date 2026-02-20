"""
AGM Store Builder - Analytics Schemas

Pydantic schemas for analytics and reporting.
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel


class OverviewStats(BaseModel):
    """Dashboard overview statistics."""
    totalRevenue: float = 0
    totalOrders: int = 0
    pendingOrders: int = 0
    completedOrders: int = 0
    totalProducts: int = 0
    activeProducts: int = 0
    totalStores: int = 0


class RecentOrder(BaseModel):
    """Recent order summary."""
    id: str
    order_number: str
    customer_name: str
    total: float
    status: str
    created_at: str


class TopProduct(BaseModel):
    """Top selling product."""
    id: str
    name: str
    sales_count: int
    revenue: float


class StoreSummary(BaseModel):
    """Store summary for dashboard."""
    id: str
    name: str
    username: str
    product_count: int = 0
    order_count: int = 0
    revenue: float = 0


class DashboardData(BaseModel):
    """Dashboard analytics data."""
    overview: OverviewStats
    recentOrders: List[RecentOrder] = []
    topProducts: List[TopProduct] = []
    stores: List[StoreSummary] = []


class ChartDataPoint(BaseModel):
    """Chart data point."""
    period: str
    revenue: float = 0
    orders: int = 0


class RevenueData(BaseModel):
    """Revenue statistics data."""
    total: float = 0
    paid: float = 0
    pending: float = 0
    thisMonth: float = 0
    lastMonth: float = 0
    growth: float = 0
    chartData: List[ChartDataPoint] = []


class StatusCount(BaseModel):
    """Order status count."""
    status: str
    count: int


class OrderStatsData(BaseModel):
    """Order statistics data."""
    total: int = 0
    pending: int = 0
    confirmed: int = 0
    processing: int = 0
    shipped: int = 0
    delivered: int = 0
    cancelled: int = 0
    averageOrderValue: float = 0
    chartData: List[StatusCount] = []


class TopSellingProduct(BaseModel):
    """Top selling product with details."""
    id: str
    name: str
    sales_count: int
    revenue: float
    stock_quantity: int


class RecentProduct(BaseModel):
    """Recently added product."""
    id: str
    name: str
    created_at: str


class ProductPerformanceData(BaseModel):
    """Product performance data."""
    totalProducts: int = 0
    activeProducts: int = 0
    outOfStock: int = 0
    lowStock: int = 0
    topSelling: List[TopSellingProduct] = []
    recentlyAdded: List[RecentProduct] = []


class TopCustomer(BaseModel):
    """Top customer by spending."""
    name: str
    email: Optional[str] = None
    order_count: int
    total_spent: float


class CustomerAnalyticsData(BaseModel):
    """Customer analytics data."""
    totalCustomers: int = 0
    newCustomers: int = 0
    returningCustomers: int = 0
    topCustomers: List[TopCustomer] = []


class DashboardResponse(BaseModel):
    """Dashboard response."""
    success: bool = True
    data: DashboardData


class RevenueResponse(BaseModel):
    """Revenue response."""
    success: bool = True
    data: RevenueData


class OrderStatsResponse(BaseModel):
    """Order stats response."""
    success: bool = True
    data: OrderStatsData


class ProductPerformanceResponse(BaseModel):
    """Product performance response."""
    success: bool = True
    data: ProductPerformanceData


class CustomerAnalyticsResponse(BaseModel):
    """Customer analytics response."""
    success: bool = True
    data: CustomerAnalyticsData
