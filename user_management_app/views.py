from rest_framework import generics, status, permissions
from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
import logging
from .models import User, Role, UserRole
from .serializers import UserSerializer, RoleSerializer
from rest_framework.permissions import AllowAny

logger = logging.getLogger(__name__)


class UserView(APIView):
    """
    API endpoint for user management.

        GET: Retrieve a list of all users.
        POST: Create a new user.
    """

    def get(self, request):
        """
        Retrieve all users from the database.
        @rtype: Response containing the list of users.
        """
        logger.debug(f'Fetching all users.')
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        logger.info(f'User data retrieved: {serializer.data}')
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Create a new user with username and password.
        Args:
            request (Request): The incoming HTTP request containing user data.
        @rtype: Response containing the created user data or errors.
        """
        logger.debug(f'Creating user with details: {request.data}')
        data = request.data
        data['password'] = make_password(data['password'])  # Hash password before saving
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            logger.debug(f'User {request.data["username"]} created successfully.')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error(f'User {request.data["username"]} creation error: {serializer.errors}')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AssignRoleView(generics.CreateAPIView):
    """
    API endpoint to assign a role to a user.

    - Requires `user_id` and `role_id` in the request body.
    - Returns an error if either the user or role does not exist.
    - Assigns the specified role to the user and logs the action.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        user_id = request.data.get("user_id")
        role_id = request.data.get("role_id")

        user = User.objects.filter(id=user_id).first()
        role = Role.objects.filter(id=role_id).first()

        if not user or not role:
            return Response({"error": "User or Role not found"}, status=status.HTTP_400_BAD_REQUEST)

        UserRole.objects.create(user=user, role=role)
        logger.debug(f'Role {role.name} assigned to {user.username}.')
        return Response({"message": "Role assigned successfully"}, status=status.HTTP_201_CREATED)


class RoleView(APIView):
    """
    API endpoint to manage roles.
    - `POST`: Create a new role (requires superuser privileges).
    - `GET`: Retrieve all roles (available to authenticated users).
    """
    permission_classes = [permissions.IsAuthenticated]  # Ensure only authenticated users access this

    def post(self, request):
        """
        Create a new role.
        - Only superusers can create new roles.
        """
        if not request.user.is_superuser:
            return Response({"error": "You do not have permission to create roles."}, status=status.HTTP_403_FORBIDDEN)

        serializer = RoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.debug(f'Role {request.data["name"]} created successfully.')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        """
        Retrieve all available roles.
        - Accessible to authenticated users.
        - Logs role retrieval action.
        """
        logger.debug('Fetching all roles.')
        roles = Role.objects.all()
        serializer = RoleSerializer(roles, many=True)
        logger.debug(f'Role data retrieved: {serializer.data}')
        return Response(serializer.data, status=status.HTTP_200_OK)
