from rest_framework import serializers
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from wefloatapi.models import Difficulty



class DifficultyView(ViewSet):

    def retrieve(self, request, pk):

        try:
            difficulty = Difficulty.objects.get(pk=pk)
        except Difficulty.DoesNotExist:
            return Response("")

        serializer = DifficultySerializer(difficulty)
        return Response(serializer.data)
      
    def list(self, request):
         
      difficulties = Difficulty.objects.all()
      
      serializer = DifficultySerializer(difficulties, many=True)
      return Response(serializer.data)


    def destroy(self, request, pk):

        difficulty = Difficulty.objects.get(pk=pk)
        difficulty.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
      
      
class DifficultySerializer(serializers.ModelSerializer):

    class Meta:
        model = Difficulty
        fields = ("id", "name")
