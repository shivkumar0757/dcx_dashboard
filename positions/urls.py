from django.urls import path
from .views import signup_view, login_view, dashboard_view, logout_view, update_token_view, PositionListView

urlpatterns = [
    path('', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('logout/', logout_view, name='logout'),
    path('update_token/', update_token_view, name='update-token'),
    path('api/positions/', PositionListView.as_view(), name='positions-list'),
]
