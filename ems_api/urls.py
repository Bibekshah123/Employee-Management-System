from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from core import views as core_views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

router = DefaultRouter()
router.register(r'users', core_views.UserViewSet, basename='user')
router.register(r'departments', core_views.DepartmentViewSet)
router.register(r'employees', core_views.EmployeeProfileViewSet, basename='employee')
router.register(r'attendance', core_views.AttendanceViewSet, basename='attendance')
router.register(r'leaves', core_views.LeaveRequestViewSet, basename='leave')

schema_view = get_schema_view(
    openapi.Info(
        title="EMS API",
        default_version='v1',
        description="Employee Management System API",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='root-swagger-redirect'),
]