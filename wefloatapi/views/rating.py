from rest_framework import serializers
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from wefloatapi.models import Rating



class RatingView(ViewSet):

    def retrieve(self, request, pk):

        try:
            rating = Rating.objects.get(pk=pk)
        except Rating.DoesNotExist:
            return Response("")

        serializer = RatingSerializer(rating)
        return Response(serializer.data)
      
    def list(self, request):
         
      ratings = Rating.objects.all()
      
      serializer = RatingSerializer(ratings, many=True)
      return Response(serializer.data)

      
class RatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rating
        fields = ("id", "value")
