from rest_framework import permissions


class IsEmployer(permissions.BasePermission):
    """
    Custom permission to allow only Employers to update company profiles.
    """

    def has_permission(self, request, view):
        # Only allow Employers to update the company profile
        return request.user and request.user.role == "Employer"


# checking the permission for listing the job whether the user is admin or employer
class IsEmployerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        # Allow all users (including candidates) to view job listings
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.role in ["Employer", "Admin"]




class IsAdminOrEmployerOrCandidate(permissions.BasePermission):
    """
    - Admins: Full access to view, create, update, and delete.
    - Employers: Can view, update, and delete job applications for their job listings.
    - Candidates: Can create new job applications, and view their own applications.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Admins have full access
        if request.user.role == "Admin":
            return True

        # Employers can view, update, and delete applications for their own job listings
        if request.user.role == "Employer":
            return obj.job.company.owner == request.user

        # Candidates can only view or create their own applications
        if request.user.role == "Candidate":
            # Candidates can view their own applications
            if view.action in ["retrieve", "list"]:
                return obj.candidate == request.user
            # Candidates can create applications but not update or delete them
            return view.action == "create"

        # Default: No access for other roles
        return False
