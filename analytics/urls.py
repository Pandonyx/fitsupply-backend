from django.urls import path
from .views import DashboardSummaryView, sales_chart_data, recent_orders

urlpatterns = [
    path('dashboard/summary/', DashboardSummaryView.as_view(), name='dashboard-summary'),
    path('dashboard/sales-chart/', sales_chart_data, name='sales-chart'),
    path('dashboard/recent-orders/', recent_orders, name='recent-orders'),
]