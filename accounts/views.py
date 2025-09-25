from django.shortcuts import render
from rest_framework import generics, permissions
from .models import CustomUser
from .serializers import UserRegisterSerializer, UserProfileSerializer

# Create your views here.
class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserRegisterSerializer

class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserProfileSerializer

    def get_object(self):
        # This view should return the current authenticated user's profile
        return self.request.user