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
        self.inventory_items = []
        for i in range(15):
            inventory = Inventory.objects.create(
                name=f"Test Item {i+1}",
                inventory_tag=self.inventory_tag,
                inventory_language=self.inventory_language,
            )
            self.inventory_items.append(inventory)
        
        self.url = reverse('inventory-list')

    def test_pagination_with_limit_offset_no_query_parameters(self):
        response = self.client.get(f"{self.url}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)
        self.assertEqual(response.data['count'], 15)
        self.assertIsNotNone(response.data['next'])
        self.assertIsNotNone(response.data['previous'])

    def test_pagination_with_limit_offset_with_limit(self):
        response = self.client.get(f"{self.url}?limit=5")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 5)
        self.assertEqual(response.data['count'], 15)
        self.assertIsNotNone(response.data['next'])
        self.assertIsNotNone(response.data['previous'])

    def test_pagination_with_limit_offset_with_offset_and_limit(self):
        response = self.client.get(f"{self.url}?limit=5&offset=5")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 5)
        self.assertEqual(response.data['count'], 15)
        self.assertIsNotNone(response.data['next'])
        self.assertIsNotNone(response.data['previous'])
