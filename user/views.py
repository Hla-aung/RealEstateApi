from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer, RegisterUserSerializer

User = get_user_model()
# Create your views here.
class RegisterView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterUserSerializer
    queryset = User

    def post(self, request):
        try:
            data = request.data

            email = data['email']
            email = email.lower()
            name = data['name']
            password = data['password']
            is_realtor = data['is_realtor']

            if len(password) >= 8:
                if not User.objects.filter(email=email).exists():
                    if is_realtor:
                        User.objects.create_realtor(name=name, email=email, password=password)

                        return Response({"message": "Realtor has been created"}, status=status.HTTP_201_CREATED)
                    else:
                        User.objects.create_user(name=name, email=email, password=password)

                        return Response({"message": "User has been created"}, status=status.HTTP_201_CREATED)

                else:
                    return Response({"message": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message": "Password must be 8 or more characters long"}, status=status.HTTP_400_BAD_REQUEST)
        
        except:
            return Response({"message": "Something went wrong when registering user"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class RetrieveUserView(GenericAPIView):
    serializer_class = UserSerializer
    queryset = User

    def get(self, request, format=None):
        try:
            user = request.user
            user = UserSerializer(user)

            return Response({
                "user": user.data
            }, status=status.HTTP_200_OK)
        except:
            return Response({"message": "Something went wrong when retrieving user"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)