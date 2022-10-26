from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account import serializers
from account.models import User
from account.serializers import UserRegistrationserializer ,UserLoginSerializer
from django.contrib.auth import authenticate  
class UserRegistrationView(APIView):
    def post(self, request, format=None):
        serializer = UserRegistrationserializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return Response({'msg':'Registration Success'})
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

# def signup(request):
#     return render(request, 'registation.html')

# class UserLoginView(APIView):
#     def post(self, request, format=None):
#         # return Response({'msg':'Login Success'})
#         serializer = UserLoginSerializer(data=request.data)
#         if serializer.if_valid(raise_exception = True):
#             email = serializer.data.get('email'),
#             password = serializer.data.get('password')
#             user = authenticate(email=email, password=password)
#             if user is not None:
#                 return Response({'msg':'Login Success'})
#             else :
#                 return Response({'error': {'non_field_errors':['Email or Password is not valid']}}, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    def post(self, request, format=None):
        serializer = UserLoginSerializer (data=request.data)
        if serializer.is_valid(raise_exception= True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            User = authenticate(email= email, password= password)
            if User is not None:
                return Response({'msg':'Login Success'})
            else :
                return Response({'error': {'non_field_errors':['Email or Password is not valid']}}, status=status.HTTP_400_BAD_REQUEST)