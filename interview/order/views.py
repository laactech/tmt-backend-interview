import datetime

from rest_framework import generics, serializers

from interview.order.models import Order, OrderTag
from interview.order.serializers import OrderSerializer, OrderTagSerializer

# Create your views here.
class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)

        start_date_query_param = self.request.query_params.get("start_date", None)
        embargo_date_query_param = self.request.query_params.get("embargo_date", None)
        if start_date_query_param and embargo_date_query_param:
            try:
                start_date = datetime.datetime.fromisoformat(start_date_query_param)
            except ValueError:
                raise serializers.ValidationError(
                    {
                        "error": "query parameter start_date must be iso formatted datetime string"
                    }
                )
            try:
                embargo_date = datetime.datetime.fromisoformat(embargo_date_query_param)
            except ValueError:
                raise serializers.ValidationError(
                    {
                        "error": "query parameter embargo_date must be iso formatted datetime string"
                    }
                )

            if start_date >= embargo_date:
                raise serializers.ValidationError(
                    {
                        "error": "start_date must be before embargo_date"
                    }
                )
                
            queryset = queryset.filter(start_date__gte=start_date, embargo_date__lte=embargo_date)
            
        return queryset

class OrderTagListCreateView(generics.ListCreateAPIView):
    queryset = OrderTag.objects.all()
    serializer_class = OrderTagSerializer
