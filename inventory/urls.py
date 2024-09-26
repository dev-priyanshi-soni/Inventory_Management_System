from django.urls import path
from .views import CreateItemView, ReadItemView, UpdateItemView, DeleteItemView

urlpatterns = [
    path('items/', CreateItemView.as_view(), name='create-item'),
    path('items/<int:item_id>/', ReadItemView.as_view(), name='read-item'),
    path('items/<int:item_id>/update/', UpdateItemView.as_view(), name='update-item'),
    path('items/<int:item_id>/delete/', DeleteItemView.as_view(), name='delete-item'),

]
