from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ModifierView,DirectOrderMenuView,ModifierCustomerView,ItemListCreateView,ItemListCustomerView,RestaurantViewSet,RestaurantEmployeeViewSet,RestaurantCustomerViewSet,CategoryCustomerView,CategoryView,ItemListCustomerView


router = DefaultRouter()

#owner CRUD restaurant
router.register('restaurant', RestaurantViewSet, basename='restaurant')
#Customer to view all restaurant and retrieve restaurant
router.register('restaurant-customer', RestaurantCustomerViewSet, basename='restaurant_customer')
#owner CRUD and employee can view
router.register('restaurant-employee', RestaurantEmployeeViewSet, basename='restaurant_employee')
#Customer to view all category and retrieve
router.register('menu-category-customer', CategoryCustomerView, basename='menu-category-customer')
router.register('menu-category', CategoryView, basename='menu-category')

router.register('item-customer', ItemListCustomerView, basename='item-customer')
router.register('item', ItemListCreateView, basename='item')

router.register('modifier-customer', ModifierCustomerView, basename='modifier-customer')
router.register('modifier', ModifierView, basename='modifier')


urlpatterns = [

    path('', include(router.urls)),
    path('detail-menu/<int:restaurant_id>/', DirectOrderMenuView.as_view(), name='direct-order-menu'),

]