from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from wefloatapi.models import Float, User, Rating, Difficulty, Tag, FloatTag

class FloatView(ViewSet):
  
  def retrieve(self, request, pk):
    
    try: 
      float = Float.objects.get(pk=pk) 
      
      tags = Tag.objects.filter(floattag_float_id=float)
      float.tags=tags.all()
      serializer = FloatSerializer(float)
      return Response(serializer.data)
    
    except Float.DoesNotExist as ex:
      return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
    
  def list(self, request):
    
    difficulty = request.query_params.get('difficulty', None)

    author_id = request.query_params.get('author', None)
    
    floats = Float.objects.all()
    
    if difficulty is not None:
      floats = floats.filter(difficulty=difficulty)
      
    if author_id is not None:
      author = User.objects.get(uid=author_id)
      floats = floats.filter(author=author)

    
    for float in floats:
      tags = Tag.objects.filter(floattag__float_id=float)
      float.tags=tags
    
    serializer = FloatSerializer(floats, many=True)
    return Response(serializer.data)
  
  def create(self, request):
    
    author = User.objects.get(uid=request.data["author"])
    rating = Rating.objects.get(pk=request.data["rating"])
    difficulty = Difficulty.objects.get(pk=request.data["difficulty"])
    
    float = Float.objects.create(
      name=request.data["name"],
      location=request.data["location"],
      author=author,
      description=request.data["description"],
      distance=request.data["distance"],
      difficulty=difficulty,
      image=request.data["image"],
      rating=rating, 
    )
    
    for tag_id in request.data["tags"]:
      tag = Tag.objects.get(pk=tag_id)
      
      FloatTag.objects.create(
        float=float,
        tag=tag
      )
    
    serializer = FloatSerializer(float)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
  
  def update(self, request, pk):
    
    author = User.objects.get(uid=request.data["author"])
    difficulty = Difficulty.objects.get(pk=request.data["difficulty"])
    rating = Rating.objects.get(pk=request.data["rating"])
    
    float = Float.objects.get(pk=pk)
    
    float.name=request.data["name"]
    float.location=request.data["location"]
    float.author=author
    float.description=request.data["description"]
    float.distance=request.data["distance"]
    float.difficulty=difficulty
    float.image=request.data["image"]
    float.rating=rating
    float.save()
    
    
    serializer = FloatSerializer(float)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  def destroy(self, request, pk):
    
    float = Float.objects.get(pk=pk)
    
    float.delete()
    return Response(None, status=status.HTTP_204_NO_CONTENT)

class TagSerializer(serializers.ModelSerializer):
  
  class Meta:
    model = Tag
    fields = ('id', 'name')
    
class FloatSerializer(serializers.ModelSerializer):
  
  tags = TagSerializer(read_only=True, many=True)
  
  class Meta:
    model = Float
    fields = ('id', 'name', 'location', 'author', 'description', 'distance', 'difficulty', 'image', 'rating', 'created_on', 'tags')
    depth = 1
