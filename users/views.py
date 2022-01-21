from django.core.mail import EmailMultiAlternatives
from django.core.paginator import EmptyPage, Paginator
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CustomUser
from .serializers import (ProfileUpdateSerializer, UpdateSerializer,
                          UserSerializer)

class UserList(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get_paginated(self, queryset, page):

        self.paginator = Paginator(queryset, 5)
        try:
            return self.paginator.page(page)
        except EmptyPage:
            return self.paginator.page(self.paginator.num_pages)

    def get(self, request, format=None):

        if request.user.groups.filter(name='adminlar').exists():
            users = CustomUser.objects.all().order_by('id')
            paginated_files = self.get_paginated(
                users, request.GET.get('page', 1))
            serializer = UserSerializer(paginated_files, many=True)
            data = {
                'total_users': self.paginator.count,
                'max_per_page': self.paginator.per_page,
                'page_range': [i for i in self.paginator.page_range],
                'results': serializer.data
            }
            return Response(data)
        else:
            return Response(
                {"detail": _(
                    "You do not have permission to perform this action.")},
                status=status.HTTP_403_FORBIDDEN
            )


class UserDetail(APIView):
    """
    Retrieve, update or delete a user instance.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return CustomUser.objects.get(id=pk)
        except CustomUser.DoesNotExist:
            return Response(
                {"detail": _("Page not found.")},
                status=status.HTTP_404_NOT_FOUND
            )

    def get(self, request, format=None):
        try:
            user = self.get_object(request.user.id)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except:
            return Response(
                {"detail": _("User not found.")},
                status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request, format=None):
        try:
            user = self.get_object(request.user.id)
            serializer = ProfileUpdateSerializer(
                user, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(
                {"detail": _("User not found.")},
                status=status.HTTP_404_NOT_FOUND
            )


class UserChangePass(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return CustomUser.objects.get(id=pk)
        except CustomUser.DoesNotExist:
            return Response(
                {"detail": _("Page not found.")},
                status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request, format=None):
        try:
            user = self.get_object(request.user.id)
            serializer = UpdateSerializer(
                user, data=request.data, context={'request': request})

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(
                {"detail": _("Page not found.")},
                status=status.HTTP_404_NOT_FOUND
            )


class UsersRegisterView(APIView):

    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if 'password' in request.data:
            if serializer.is_valid():
                password = request.data["password"]
                if len(password) < 8:
                    return Response(
                        {"detail": _(
                            "Password length should not be less than 8 characters.")},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(
                {"detail": _("Password field is required.")},
                status=status.HTTP_400_BAD_REQUEST
            )


