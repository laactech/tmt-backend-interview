from rest_framework import generics, mixins
from rest_framework.generics import GenericAPIView

from interview.order.models import Order, OrderTag
from interview.order.serializers import OrderSerializer, OrderTagSerializer, DeactivateOrderSerializer


# Create your views here.
class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    

class OrderTagListCreateView(generics.ListCreateAPIView):
    queryset = OrderTag.objects.all()
    serializer_class = OrderTagSerializer


class DeactivateOrderView(mixins.UpdateModelMixin, GenericAPIView):
    queryset = Order.objects.all()
    serializer_class = DeactivateOrderSerializer
