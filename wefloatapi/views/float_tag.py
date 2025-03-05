from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from wefloatapi.models import FloatTag, Tag, Float

class FloatTagView(ViewSet):
  
  def retrieve(self, request, pk):

    try:
      float_tag = FloatTag.objects.get(pk=pk)
      serializer = FloatTagSerializer(float_tag)
      return Response(serializer.data)
    except FloatTag.DoesNotExist as ex:
      return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
    
  def list(self, request):

    float_tag = FloatTag.objects.all()
    
    serializer = FloatTagSerializer(float_tag, many=True)
    return Response(serializer.data)
  
  def create(self, request):

    float = Float.objects.get(pk=request.data["float"])
    tag = Tag.objects.get(pk=request.data["tag"])
    
    float_tag = FloatTag.objects.create(
      float=float,
      tag=tag,
    )
    serializer = FloatTagSerializer(float_tag)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
  
  def update(self, request, pk):

    float = Float.objects.get(pk=request.data["float"])
    tag = Tag.objects.get(pk=request.data["tag"])
    
    float_tag = FloatTag.objects.get(pk=pk)
    float_tag.float = float
    float_tag.tag = tag
    float_tag.save()
    
    serializer = FloatTagSerializer(float_tag)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  def destroy(self, request, pk):
    float_tag = FloatTag.objects.get(pk=pk)
    float_tag.delete()
    return Response(None, status=status.HTTP_204_NO_CONTENT)
  
class FloatTagSerializer(serializers.ModelSerializer):

  class Meta:
    model = FloatTag
    fields = ('id', 'float', 'tag')
    depth = 1
    