import datetime
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from interview.inventory.models import Inventory, InventoryTag, InventoryLanguage


class TestInventoryListCreateView(APITestCase):
    def setUp(self):
        self.inventory_tag = InventoryTag.objects.create(name="test")
        self.inventory_language = InventoryLanguage.objects.create(
            name="probably english"
        )
        self.inventory1 = Inventory.objects.create(
            name="Test Item 1",
            tag=self.inventory_tag,
            language=self.inventory_language,
            metadata={},
            created_at=datetime.datetime(2024, 1, 1, tzinfo=datetime.UTC),
        )
        self.inventory2 = Inventory.objects.create(
            name="Test Item 2",
            tag=self.inventory_tag,
            language=self.inventory_language,
            metadata={},
            created_at=datetime.datetime(2024, 2, 1, tzinfo=datetime.UTC),
        )
        self.inventory3 = Inventory.objects.create(
            name="Test Item 3",
            tag=self.inventory_tag,
            language=self.inventory_language,
            metadata={},
            created_at=datetime.datetime(2024, 3, 1, tzinfo=datetime.UTC),
        )
        self.url = reverse("inventory-list")

    def test_list_inventory_with_created_at_filter(self):
        filter_date = "2024-02-01T00:00:00+00:00"
        response = self.client.get(f"{self.url}?created_at={filter_date}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        returned_ids = {item["id"] for item in response.data}
        expected_ids = {self.inventory1.id, self.inventory2.id}
        self.assertEqual(returned_ids, expected_ids)

    def test_list_inventory_with_invalid_created_at_format(self):
        invalid_date = "2024-13-45"
        response = self.client.get(f"{self.url}?created_at={invalid_date}")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        self.assertIn(
            "query parameter created_at must be iso formatted datetime string",
            response.data["error"],
        )

    def test_list_inventory_without_created_at_filter(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
