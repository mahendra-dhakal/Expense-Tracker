from .models import ExpenseIncome
from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth import authenticate




class UserSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True)

    class Meta:
        model=User
        fields=['id','first_name','last_name','username','email','password']



class UserRegistrationSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True,min_length=8)
    confirm_password=serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model=User
        fields=['id','first_name','last_name','username','email','password','confirm_password']
    
    def validate(self,attrs):
        if attrs['password']!=attrs['confirm_password']:
            raise serializers.ValidationError("Password don't match!")
        return attrs
    
    def create(self,validated_data):
        validated_data.pop('confirm_password')
        user=User.objects.create_user(**validated_data)
        return user

class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def validate(self, attrs):
        
        username = (attrs.get('username') or '').strip().lower()
        email = (attrs.get('email') or '').strip().lower()
        password = attrs.get('password')

        if not (username or email):
            raise serializers.ValidationError('Provide either username or email')
        if username and email:
            raise serializers.ValidationError('Provide only one of username or email')

        try:
            user = User.objects.get(Q(username__iexact=username) | Q(email__iexact=email))    
        except User.DoesNotExist:
            raise serializers.ValidationError('Invalid credentials!')

        authenticated_user = authenticate(username=user.username, password=password)

        if not authenticated_user:
            raise serializers.ValidationError('Invalid credentials!')

        attrs['user'] = authenticated_user
        return attrs
    
    

class ExpenseIncomeSerializer(serializers.ModelSerializer):
    total=serializers.SerializerMethodField()
    
    class Meta:
        model=ExpenseIncome
        fields='__all__'
        read_only_fields= ['user','total','created_at','updated_at']
    
    
    def get_total(self,obj):
        return obj.total
    