from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User, Department, EmployeeProfile, Attendance, LeaveRequest

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name', 'role']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        user = super().create(validated_data)
        return user


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name', 'description']


class EmployeeProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = EmployeeProfile
        fields = ['id', 'user', 'department', 'position', 'salary', 'date_joined', 'phone']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create(**{**user_data, 'password': make_password(user_data['password'])})
        profile = EmployeeProfile.objects.create(user=user, **validated_data)
        return profile


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['id', 'user', 'date', 'status', 'note']
        read_only_fields = ['id']


class LeaveRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveRequest
        fields = ['id', 'user', 'start_date', 'end_date', 'reason', 'status', 'created_at', 'reviewed_by']
        read_only_fields = ['status', 'created_at', 'reviewed_by']