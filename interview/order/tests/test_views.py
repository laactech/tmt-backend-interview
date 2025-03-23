import datetime
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from interview.inventory.models import Inventory, InventoryTag, InventoryLanguage
from interview.order.models import Order


class TestOrderListCreateView(APITestCase):
    def setUp(self):
        # Create a test inventory
        self.inventory_tag = InventoryTag.objects.create(name="test")
        self.inventory_language = InventoryLanguage.objects.create(
            name="probably english"
        )
        self.inventory = Inventory.objects.create(
            name="Test Item 1",
            tag=self.inventory_tag,
            language=self.inventory_language,
            metadata={},
            created_at=datetime.datetime(2024, 1, 1, tzinfo=datetime.UTC),
        )
        self.order1 = Order.objects.create(
            inventory=self.inventory,
            start_date=datetime.date(2024, 1, 1),
            embargo_date=datetime.date(2024, 2, 1)
        )
        self.order2 = Order.objects.create(
            inventory=self.inventory,
            start_date=datetime.date(2024, 2, 1),
            embargo_date=datetime.date(2024, 3, 1)
        )
        self.url = reverse('order-list')

    def test_filter_with_valid_dates(self):
        response = self.client.get(
            f"{self.url}?start_date=2024-01-15T00:00:00+00:00&embargo_date=2024-02-15T00:00:00+00:00"
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_filter_with_invalid_date_format(self):
        response = self.client.get(
            f"{self.url}?start_date=2024-13-45&embargo_date=2024-02-15T00:00:00+00:00"
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertIn('query parameter start_date must be iso formatted datetime string', response.data['error'])

    def test_filter_with_start_date_after_embargo_date(self):
        response = self.client.get(
            f"{self.url}?start_date=2024-02-15T00:00:00+00:00&embargo_date=2024-01-15T00:00:00+00:00"
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'start_date must be before embargo_date') 