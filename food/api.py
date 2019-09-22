from .models import Food
from .serializer import FoodSerializer
from rest_framework import generics, status, permissions
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
    permission_classes = [
        permissions.AllowAny,
    ]
    serializer_class = FoodSerializer

    def get_queryset(self):
        queryset = Food.objects.all()
        if(self.request.query_params):
            food_name = self.request.query_params.get('food_name', '')
            return queryset.filter(name__icontains=food_name)
        return queryset
