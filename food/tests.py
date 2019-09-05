from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from .models import Food
from .serializer import FoodSerializer
from django.urls import reverse

class AddFoodTest(APITestCase):
    client = APIClient()

    @staticmethod
    def create_food(name="", brand="", energy_value=0, fats=0, saturated_fats=0, carbohydrates=0, sugars=0, proteins=0, salt=0):
        if name != "" and brand != "" and energy_value != 0 and fats != 0 and saturated_fats != 0 and carbohydrates != 0 and sugars != 0 and proteins != 0 and salt != 0:
            Food.objects.create(name=name, brand=brand, energy_value=energy_value, fats=fats, saturated_fats=saturated_fats, carbohydrates=carbohydrates, sugars=sugars, proteins=proteins, salt=salt)

    def setUp(self):
        self.create_food("Banan", "Firma", 100, 5, 2, 10, 20, 10, 1)
        self.create_food("Jajko", "Firma1", 200, 51, 24, 510, 920, 910, 16)
        self.create_food("Banan", "Firma2", 300, 52, 26, 150, 200, 190, 15)
        self.create_food("Banan", "Firma3", 400, 59, 62, 105, 201, 109, 14)
        self.create_food("Banan", "Firma4", 500, 41, 25, 106, 210, 104, 13)
        self.create_food("Banan", "Firma5", 600, 12, 52, 160, 120, 140, 12)

class GetAllFoodsTest(AddFoodTest):

    def test_get_all_foods(self):
        response = self.client.get(
            reverse("foods-all")
        )

        expected = Food.objects.all()
        serialized = FoodSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
