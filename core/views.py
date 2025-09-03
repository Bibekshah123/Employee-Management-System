from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import User, Department, EmployeeProfile, Attendance, LeaveRequest
from .serializers import (
    UserSerializer, DepartmentSerializer, EmployeeProfileSerializer,
    AttendanceSerializer, LeaveRequestSerializer
)
from .permissions import IsAdminOrHR, IsManagerOrAbove

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]  # allow registration

    def get_permissions(self):
        if self.action in ['create']:
            return [permissions.AllowAny()]
        if self.action in ['list', 'destroy', 'update', 'partial_update']:
            return [IsAdminOrHR()]
        return [permissions.IsAuthenticated()]


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all().order_by('name')
    serializer_class = DepartmentSerializer
    permission_classes = [IsAdminOrHR]


class EmployeeProfileViewSet(viewsets.ModelViewSet):
    serializer_class = EmployeeProfileSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role in ['admin', 'hr']:
            return EmployeeProfile.objects.select_related('user', 'department').all()
        if user.role == 'manager':
            # Managers can see employees in their department (if they have a profile)
            try:
                dept = user.profile.department
                return EmployeeProfile.objects.select_related('user', 'department').filter(department=dept)
            except EmployeeProfile.DoesNotExist:
                return EmployeeProfile.objects.none()
        return EmployeeProfile.objects.filter(user=user)

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminOrHR()]
        return [permissions.IsAuthenticated()]


class AttendanceViewSet(viewsets.ModelViewSet):
    serializer_class = AttendanceSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role in ['admin', 'hr', 'manager']:
            return Attendance.objects.select_related('user').all()
        return Attendance.objects.filter(user=user)

    def get_permissions(self):
        if self.action in ['create']:  # employees can mark their own attendance
            return [permissions.IsAuthenticated()]
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsManagerOrAbove()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        # If user not admin/hr/manager, force attendance to current user
        user = self.request.user
        data_user = serializer.validated_data.get('user')
        if user.role == 'employee' or data_user is None:
            serializer.save(user=user)
        else:
            serializer.save()


class LeaveRequestViewSet(viewsets.ModelViewSet):
    serializer_class = LeaveRequestSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role in ['admin', 'hr', 'manager']:
            return LeaveRequest.objects.select_related('user', 'reviewed_by').all()
        return LeaveRequest.objects.filter(user=user)

    def get_permissions(self):
        if self.action in ['create', 'list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        if self.action in ['approve', 'reject', 'update', 'partial_update', 'destroy']:
            return [IsManagerOrAbove()]
        return [permissions.IsAuthenticated()]

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        leave = self.get_object()
        leave.status = 'approved'
        leave.reviewed_by = request.user
        leave.save()
        return Response({'status': 'approved'})

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        leave = self.get_object()
        leave.status = 'rejected'
        leave.reviewed_by = request.user
        leave.save()
        return Response({'status': 'rejected'})