from rest_framework.permissions import BasePermission

from authentication.models import User


class VacancyCreatePermission(BasePermission):
    message = 'Adding vacancies for non hr user not allowed'
    def has_permission(self, request, view):
        if request.user.role == User.HR:
            return True
        return False