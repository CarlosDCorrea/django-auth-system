from django.contrib.auth import authenticate
from django.shortcuts import render, redirect

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response 
from rest_framework.authtoken.models import Token

from .serializers import UserSerializer
from .models import User

from ..email_app.service import create_email


@api_view(http_method_names=['POST'])
def create(request):
    serializer = UserSerializer(data=request.data)

    response = Response()

    if serializer.is_valid():
        user = serializer.create(serializer.validated_data)

        response_email_app = create_email(user.username, user.id, request)
        print(response_email_app)
        response.data = {"message": f"usuario {user.username} creado satisfactoriamente, te hemos enviado un correo para que valides tu cuenta"}
        response.status_code = status.HTTP_201_CREATED
    else:
        response.data = {'message_error': serializer.errors}
        response.status_code = status.HTTP_400_BAD_REQUEST

    return response

@api_view(http_method_names=['POST'])
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
    except Exception as e:
        response.data = str(e)
        response.status_code = status.HTTP_400_BAD_REQUEST

        return response 
    
    return response

#@TODO change for list all
@api_view(http_method_names=['GET'])
@permission_classes([IsAuthenticated])
def list(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)

    response = Response()
    response.data = serializer.data 
    response.status_code = status.HTTP_200_OK
    
    return response

@api_view(['GET'])
def activate(request):
    print('being called')
    return redirect('activate-user-success')

@api_view()
def activate_user_success(request):
    print(f'request.data {request.data}')
    return render(request, "user/validate_user.html")


""" user_id = request.query_params['id']

user = User.objects.get(id=user_id)

if user:
    user.is_active = True
    user.save()
    redirect('activate-user-success', request)
else:
    raise User.DoesNotExist('There is not user with the id {}'.format(user_id)) """