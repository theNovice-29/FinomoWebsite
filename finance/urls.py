from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name = 'finance'
urlpatterns = [
    #path('', views.finance_list, name='finance_list'),
    path('', views.dashboard, name='dashboard'),
    path('transactions/', views.transaction, name='transactions'),
    path('totalBudget/', views.totalBudget, name='totalBudget'),
    path('search-results/', views.searchResults, name='search-results'),
    path('updateTransaction/<str:transaction_number>/', views.updateTransaction, name='updateTransaction'),
    path('updateDeleteTransaciton/', views.updateDeleteTransaciton, name='updateDeleteTransaciton'),
    path('search_transactions/', views.search_transactions, name='search_transactions'),
    path('settlements/<int:settlement_id>/', views.settlement_detail, name='settlement_detail'),
    path('settlements/<int:settlement_id>/post_comment/', views.post_comment, name='post_comment'),
    path('comments/<int:comment_id>/edit/', views.edit_comment, name='comment_detail'),
    path('comments/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
]
