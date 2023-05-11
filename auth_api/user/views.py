from .serializers import UserSerializer
from .models import User

from django.contrib.auth import authenticate

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response 
from rest_framework.authtoken.models import Token


@api_view(http_method_names=['POST'])
def create(request):
    serializer = UserSerializer(data=request.data)

    response = Response()

    if serializer.is_valid():
        user = serializer.create(serializer.validated_data)

        response.data = {"message": f"usuario {user.username} creado satisfactoriamente"}
        response.status = status.HTTP_201_CREATED
    else: 
        response.data = serializer.errors
        response.status = status.HTTP_400_BAD_REQUEST

    return response

@api_view(http_method_names=['GET'])
def login(request): 
    email = request.data['email']
    password = request.data['password']

    response = Response()

    try: 
        user = authenticate(email=email, password=password)

        if not user:
            raise User.DoesNotExist('No hay ningún usuario registrado con el correo {}'.format(email))
        
        token = Token.objects.get(user=user)
        response.data = {'Token': token.key}
        response.status = status.HTTP_201_CREATED
    except Exception as e:
        response.data = str(e)
        response.status = status.HTTP_400_BAD_REQUEST

        return response 
    
    return response

@api_view(http_method_names=['GET'])
@permission_classes([IsAuthenticated])
def list(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)

    response = Response()
    response.data = serializer.data 
    response.status = status.HTTP_200_OK
    
    return response
