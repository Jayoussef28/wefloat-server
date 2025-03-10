from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from wefloatapi.models import Comment, User, Rating, Float


class CommentView(ViewSet):

    def retrieve(self, request, pk):

        try:
            comment = Comment.objects.get(pk=pk)
            serializer = CommentSerializer(comment)
            return Response(serializer.data)
        except Comment.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
    
        comments = Comment.objects.all()
        
        float = request.query_params.get('float', None)
        
        if float is not None:
            comments = comments.filter(float=float)
        
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
      
    def create(self, request):

      commenter = User.objects.get(pk=request.data["commenter"])
      float = Float.objects.get(pk=request.data["float"])
      rating = Rating.objects.get(pk=request.data["rating"])

      comment = Comment.objects.create(
          float=float,
          commenter=commenter,
          rating=rating,
          body=request.data["body"],
      )
      serializer = CommentSerializer(comment)
      return Response(serializer.data, status=status.HTTP_201_CREATED)
  
    def update(self, request, pk):
      
        commenter = User.objects.get(pk=request.data["commenter"])
        float = Float.objects.get(pk=request.data["float"])
        rating = Rating.objects.get(pk=request.data["rating"])
    
        comment = Comment.objects.get(pk=pk)
        comment.float=float
        comment.commenter=commenter
        comment.rating=rating
        comment.body=request.data["body"]
        comment.save()
        
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def destroy(self, request, pk):
        comment = Comment.objects.get(pk=pk)
        comment.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
  
       
class CommentSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = Comment
        fields = ('id', 'float', 'commenter', 'rating', 'body', 'created_on')
    
