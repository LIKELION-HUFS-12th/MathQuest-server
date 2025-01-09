from dj_rest_auth.registration.serializers import RegisterSerializer
from allauth.account.adapter import get_adapter
from rest_framework import serializers
from .models import CustomUser

class CustomRegisterSerializer(RegisterSerializer):
    name = serializers.CharField(max_length=100)
    birthdate = serializers.CharField(max_length=100) # 날짜 필드
    school = serializers.CharField(max_length=50)
    grade = serializers.CharField(max_length=50)

    def get_cleaned_data(self):
        super(CustomRegisterSerializer, self).get_cleaned_data()
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'password2': self.validated_data.get('password2', ''),
            'name': self.validated_data.get('name', ''),
            'birthdate': self.validated_data.get('birthdate', ''),
            'school': self.validated_data.get('school', ''),
            'grade': self.validated_data.get('grade', ''),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user.username = self.cleaned_data.get('username')
        user.name = self.cleaned_data.get('name')
        user.birthdate = self.cleaned_data.get('birthdate')
        user.school = self.cleaned_data.get('school')
        user.grade = self.cleaned_data.get('grade')
        user.save()
        adapter.save_user(request, user, self)
        return user

class CustomUserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'name', 'birthdate', 'school', 'grade']


from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    class Meta:
        model = User
        fields = ['username', 'password', 'name', 'school', 'grade']

    def update(self, instance, validated_data):
        # Username 업데이트
        instance.username = validated_data.get('username', instance.username)
        
        # Password 업데이트
        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)

        # Name, School, Grade 업데이트
        instance.name = validated_data.get('name', instance.name)
        instance.school = validated_data.get('school', instance.school)
        instance.grade = validated_data.get('grade', instance.grade)
        
        instance.save()
        return instance
