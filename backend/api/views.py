from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate
from .models import User, TestNSI, TestResults
from .serializers import UserSerializer, RegisterSerializer, TestNSISerializer, TestResultsSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        serializer = RegisterSerializer(data=request.data)  # Используем RegisterSerializer
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        print(f"Попытка входа: username={username}, password={password}")
        user = authenticate(username=username, password=password)
        print(f"Результат аутентификации: {user}")
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response({'error': 'Неверные данные'}, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data)


class ResultsViewSet(viewsets.ModelViewSet):
    queryset = TestResults.objects.all()
    serializer_class = TestResultsSerializer

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def add_result(self, request):
        if not request.user.is_authenticated:
            return Response({"error": "User is not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

        print(f"User: {request.user}, Data: {request.data}")
        data = request.data.copy()

        serializer = TestResultsSerializer(data=data, context={'user': request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(f"Serializer errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TestViewSet(viewsets.ModelViewSet):
    queryset = TestNSI.objects.all()
    serializer_class = TestNSISerializer

    @action(detail=False, methods=['post'], permission_classes=[IsAdminUser])
    def add_test(self, request):
        if not request.user.is_staff:
            return Response("Only for admins", status=status.HTTP_403_FORBIDDEN)
        serializer = TestNSISerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
