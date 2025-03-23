import datetime
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from interview.inventory.models import Inventory, InventoryTag, InventoryLanguage
from interview.order.models import Order


class TestDeactivateOrderView(APITestCase):
    def setUp(self):
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
        self.order = Order.objects.create(inventory=self.inventory,
                                          start_date=datetime.datetime(2024, 1, 1, tzinfo=datetime.UTC),
                                          embargo_date=datetime.datetime(2024, 2, 1, tzinfo=datetime.UTC))
        self.url = reverse("order-deactivate")

    def test_deactivate_order(self):
        response = self.client.patch(self.url, data={"is_active": False})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.order.refresh_from_db()
        self.assertFalse(self.order.is_active)
