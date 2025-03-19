from wefloatapi.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['POST'])
def check_user(request):
    uid = request.data['uid']
    user = User.objects.filter(uid=uid).first()

    if user is not None:
        data = {
            'id': user.id,
            'username': user.username,
            'firstName': user.first_name,
            'lastName': user.last_name,
            'image': user.image,
            'bio': user.bio,
            'uid': user.uid,

        }
        return Response(data)
    else:
        data = {'valid': False}
        return Response(data)


@api_view(['POST'])
def register_user(request):
    user = User.objects.create(
        image=request.data['image'],
        username=request.data['username'],
        bio=request.data['bio'],
        uid=request.data['uid'],
        first_name=request.data['firstName'],
        last_name=request.data['lastName'],
    )

    data = {
        'id': user.id,
        'uid': user.uid,
        'bio': user.bio,
        'firstName': user.first_name,
        'lastName': user.last_name,
        'image': user.image
    }

    return Response(data)
