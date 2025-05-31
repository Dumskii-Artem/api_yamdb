from rest_framework import status
from rest_framework.response import Response


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        self.permission_classes = [permissions.IsAdminUser]
        self.check_permissions(request)
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        self.permission_classes = [permissions.IsAdminUser]
        self.check_permissions(request)
        return super().destroy(request, *args, **kwargs)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        self.permission_classes = [permissions.IsAdminUser]
        self.check_permissions(request)
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        self.permission_classes = [permissions.IsAdminUser]
        self.check_permissions(request)
        return super().destroy(request, *args, **kwargs)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'partial_update', 'update']:
            return TitleSerializer
        return TitleDetailSerializer

    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        self.permission_classes = [permissions.IsAdminUser]
        self.check_permissions(request)
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        self.permission_classes = [permissions.IsAdminUser]
        self.check_permissions(request)
        return super().destroy(request, *args, **kwargs)
