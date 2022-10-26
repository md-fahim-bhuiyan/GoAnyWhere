from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from account.serializers import UserRegistrationserializer

class UserRegistrationView(APIView):
    def post(self, request, format=None):
        serializer = UserRegistrationserializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return Response({'msg':'Registration Success'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)