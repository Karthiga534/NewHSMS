from typing import Optional
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.conf import settings


User = get_user_model()


class FixedRoleBackend(BaseBackend):
    """Authenticate Admin and Warden via fixed credentials in settings.FIXED_LOGINS.

    - settings.FIXED_LOGINS = {
    -   'admin': {'username': 'admin', 'password': 'admin123'},
    -   'warden': {'username': 'warden', 'password': 'warden123'},
    - }
    """

    def authenticate(self, request, username: Optional[str] = None, password: Optional[str] = None, **kwargs):
        fixed_cfg = getattr(settings, 'FIXED_LOGINS', {}) or {}
        if not username or not password:
            return None

        # Check admin fixed login
        admin_cfg = fixed_cfg.get('admin') or {}
        if username == admin_cfg.get('username') and password == admin_cfg.get('password'):
            user, _ = User.objects.get_or_create(username=admin_cfg['username'], defaults={
                'email': 'admin@hsms.local',
                'role': User.Roles.ADMIN,
                'is_staff': True,
                'is_superuser': True,
            })
            # Ensure flags are correct even if user existed
            changed = False
            if user.role != User.Roles.ADMIN:
                user.role = User.Roles.ADMIN; changed = True
            if not user.is_staff:
                user.is_staff = True; changed = True
            if not user.is_superuser:
                user.is_superuser = True; changed = True
            if changed:
                user.save(update_fields=['role', 'is_staff', 'is_superuser'])
            return user

        # Check warden fixed login
        warden_cfg = fixed_cfg.get('warden') or {}
        if username == warden_cfg.get('username') and password == warden_cfg.get('password'):
            user, _ = User.objects.get_or_create(username=warden_cfg['username'], defaults={
                'email': 'warden@hsms.local',
                'role': User.Roles.WARDEN,
                'is_staff': True,
                'is_superuser': False,
            })
            changed = False
            if user.role != User.Roles.WARDEN:
                user.role = User.Roles.WARDEN; changed = True
            if not user.is_staff:
                user.is_staff = True; changed = True
            if user.is_superuser:
                user.is_superuser = False; changed = True
            if changed:
                user.save(update_fields=['role', 'is_staff', 'is_superuser'])
            return user

        return None

    def get_user(self, user_id: int):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


class StudentOnlyModelBackend(BaseBackend):
    """Allow normal username/password for users with role=STUDENT only.
    Admin/Warden will be handled by FixedRoleBackend.
    """

    def authenticate(self, request, username: Optional[str] = None, password: Optional[str] = None, **kwargs):
        if not username or not password:
            return None
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None
        if user.role != User.Roles.STUDENT:
            return None
        if user.check_password(password):
            return user
        return None

    def get_user(self, user_id: int):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

