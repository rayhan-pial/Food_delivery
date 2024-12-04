from rest_framework.viewsets import ModelViewSet,ReadOnlyModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from . serializers import RestaurantSerializer, RestaurantEmployeeSerializer, CategorySerializer, ItemSerializer, ModifierSerializer
from .models import Restaurant, RestaurantEmployee, Category, Item, Modifier

from .custompermissions  import IsOwnerOrEmployee, IsOwner, IsCustomer




class RestaurantCustomerViewSet(ReadOnlyModelViewSet):

    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsCustomer]


class RestaurantViewSet(ModelViewSet):
    serializer_class = RestaurantSerializer
    permission_classes = [IsOwner]

    def get_queryset(self):
        return Restaurant.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class RestaurantEmployeeViewSet(ModelViewSet):
    serializer_class = RestaurantEmployeeSerializer
    permission_classes = [IsOwnerOrEmployee]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'owner':
            return RestaurantEmployee.objects.filter(restaurant__owner=user)
        elif user.role == 'employee':
            return RestaurantEmployee.objects.filter(employee=user)
        return Response({"detail": "You do not have permission."}, status=404)

    def perform_create(self, serializer):

        user = self.request.user
        restaurant=self.request.data.get('restaurant')
        if user.role != 'owner':
            return Response({"detail": "You do not have permission."}, status=404)
        elif Restaurant.objects.filter(id=restaurant, owner=user).exists():
            serializer.save()
        return Response({"detail": "You do not have permission."}, status=404)

    def perform_update(self, serializer):
        user = self.request.user
        instance = serializer.instance
        if user.role != 'owner':
            return Response({"detail": "You do not have permission."}, status=404)
        elif Restaurant.objects.filter(employees=instance.id, owner=user).exists():
            serializer.save()
        return Response({"detail": "You do not have permission."}, status=404)

    def perform_destroy(self, instance):
        user = self.request.user
        if user.role != 'owner':
            return Response({"detail": "You do not have permission."}, status=404)
        elif Restaurant.objects.filter(employees=instance.id, owner=user).exists():
            instance.delete()
        return Response({"detail": "You do not have permission."}, status=404)


class CategoryCustomerView(ReadOnlyModelViewSet):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsCustomer]



class CategoryView(ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsOwnerOrEmployee]

    def get_queryset(self):
        user = self.request.user

        if user.role == 'owner':
            return Category.objects.filter(restaurant__owner=user)
        elif user.role == 'employee':
            return Category.objects.filter(restaurant__employees__employee=user)
        return Response({"detail": "You do not have permission."}, status=404)


    def perform_create(self, serializer):
        user = self.request.user
        restaurant=self.request.data.get('restaurant')
        if Restaurant.objects.filter(id=restaurant, owner=user).exists() or RestaurantEmployee.objects.filter(id=restaurant, employee=user).exists():
            serializer.save()
        return Response({"detail": "You do not have permission."}, status=404)


    def perform_update(self, serializer):
        user = self.request.user
        instance = serializer.instance
        if Restaurant.objects.filter(categories=instance.id, owner=user).exists() or RestaurantEmployee.objects.filter(restaurant__categories=instance.id, employee=user).exists():
            serializer.save()
        return Response({"detail": "You do not have permission."}, status=404)

    def perform_destroy(self, instance):
        user = self.request.user
        if Restaurant.objects.filter(categories=instance.id, owner=user).exists() or RestaurantEmployee.objects.filter(restaurant__categories=instance.id, employee=user).exists():
            instance.delete()
        return Response({"detail": "You do not have permission."}, status=404)



class ItemListCustomerView(ReadOnlyModelViewSet):

    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsCustomer]



class ItemListCreateView(ModelViewSet):
    serializer_class = ItemSerializer
    permission_classes = [IsOwnerOrEmployee]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'owner':
            return Item.objects.filter(menu_category__restaurant__owner=user)
        elif user.role == 'employee':
            return Item.objects.filter(menu_category__restaurant__employees__employee=user)
        return Response({"detail": "You do not have permission."}, status=404)

    def perform_create(self, serializer):
        user = self.request.user
        category=self.request.data.get('menu_category')
        if Restaurant.objects.filter(categories=category, owner=user).exists() or RestaurantEmployee.objects.filter(restaurant__categories=category,employee=user).exists():
            serializer.save()
        return Response({"detail": "You do not have permission."}, status=404)

    def perform_update(self, serializer):
        user = self.request.user
        instance = serializer.instance
        if Restaurant.objects.filter(categories__items=instance.id, owner=user).exists() or RestaurantEmployee.objects.filter(restaurant__categories__items=instance.id,employee=user).exists():
            serializer.save()
        return Response({"detail": "You do not have permission."}, status=404)


    def perform_destroy(self, instance):
        user = self.request.user

        if Restaurant.objects.filter(categories__items=instance.id, owner=user).exists() or RestaurantEmployee.objects.filter(restaurant__categories__items=instance.id,employee=user).exists():
            instance.delete()
        return Response({"detail": "You do not have permission."}, status=404)


class ModifierCustomerView(ReadOnlyModelViewSet):

    queryset = Modifier.objects.all()
    serializer_class = ModifierSerializer
    permission_classes = [IsCustomer]


class ModifierView(ModelViewSet):
    serializer_class = ModifierSerializer
    permission_classes = [IsOwnerOrEmployee]

    def get_queryset(self):
        user = self.request.user

        if user.role == 'owner':
            return Modifier.objects.filter(item__menu_category__restaurant__owner=user)
        elif user.role == 'employee':
            return Modifier.objects.filter(item__menu_category__restaurant__employees__employee=user)
        return Response({"detail": "You do not have permission."}, status=404)


    def perform_create(self, serializer):
        user = self.request.user
        item=self.request.data.get('item')
        if Restaurant.objects.filter(categories__items=item, owner=user).exists() or RestaurantEmployee.objects.filter(restaurant__categories__items=item,employee=user).exists():
            serializer.save()
        return Response({"detail": "You do not have permission."}, status=404)


    def perform_update(self, serializer):
        user = self.request.user
        instance = serializer.instance
        if Restaurant.objects.filter(categories__items__modifiers=instance.id, owner=user).exists() or RestaurantEmployee.objects.filter(restaurant__categories__items__modifiers=instance.id,employee=user).exists():
            serializer.save()
        return Response({"detail": "You do not have permission."}, status=404)


    def perform_destroy(self, instance):
        user = self.request.user
        if Restaurant.objects.filter(categories__items__modifiers=instance.id, owner=user).exists() or RestaurantEmployee.objects.filter(restaurant__categories__items__modifiers=instance.id,employee=user).exists():
            instance.delete()
        return Response({"detail": "You do not have permission."}, status=404)



class DirectOrderMenuView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, restaurant_id):
        try:
            restaurant = Restaurant.objects.get(id=restaurant_id)
        except Restaurant.DoesNotExist:
            return Response({"detail": "Restaurant not found."}, status=404)

        serializer = RestaurantSerializer(restaurant)
        return Response(serializer.data)


