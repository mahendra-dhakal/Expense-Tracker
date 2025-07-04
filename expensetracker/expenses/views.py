from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions,status
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from .serializers import UserSerializer, UserRegistrationSerializer, UserLoginSerializer,ExpenseIncomeSerializer
from .models import ExpenseIncome
from rest_framework.viewsets import ModelViewSet
from .permissions import IsOwnerOrSuperuser
# Create your views here.


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def UserRegisterView(request):
    serializer=UserRegistrationSerializer(data=request.data)

    if serializer.is_valid():
        user=serializer.save()
        refresh=RefreshToken.for_user(user)
        return Response({
            'user':UserRegistrationSerializer(user).data,
            'refresh':str(refresh),
            'access':str(refresh.access_token),
            'message':'Registration successfull!'
        },status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
        
        
@api_view(['POST']) 
@permission_classes([permissions.AllowAny])  
def UserLoginView(request):

    serializer=UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user=serializer.validated_data['user']
        refresh=RefreshToken.for_user(user)   
        return Response({
            'user': UserSerializer(user).data,
            'refresh':str(refresh),
            'access':str(refresh.access_token)
        },status=status.HTTP_200_OK
        )     
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)




class ExpenseIncomeView(ModelViewSet):
    serializer_class=ExpenseIncomeSerializer
    permission_classes=[permissions.IsAuthenticated,IsOwnerOrSuperuser]
    
    def get_queryset(self):
        if self.request.user.is_superuser:
            return ExpenseIncome.objects.all()
        return ExpenseIncome.objects.filter(user=self.request.user)
    
    def perform_create(self,serializer):
        serializer.save(user=self.request.user)