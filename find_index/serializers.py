from rest_framework import serializers
from .models import *

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'phone_no', 'password']
        extra_kwargs = {
            'first_name' : {'required':True},
            'last_name' : {'required':True},
            'phone_no' : {'required':True}
            }


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
    
class LogSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.email')
    class Meta:
        model = Log
        fields = ["type", "sub_type", "shift_name", "description", "created_by", "date"]
        read_only_fields = ['date']


class FindIndexSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='email', read_only=True)
    class Meta:
        model = FindIndex
        fields = ['log_data', 'user']
   
        
class SendMailSerializer(serializers.Serializer):
    send_to = serializers.ListField(child = serializers.IntegerField(min_value = 0, max_value = 100))