from .models import Food
from .serializer import FoodSerializer
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

class AddFoodAPI(APIView):

    def post(self, request):
        serializer = FoodSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)

class ListFoodAPI(generics.ListAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer