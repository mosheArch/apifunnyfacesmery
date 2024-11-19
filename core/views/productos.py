from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from ..models import Producto, PedidoProducto
from ..serializers import ProductoSerializer, PedidoProductoSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

class PedidoProductoViewSet(viewsets.ModelViewSet):
    serializer_class = PedidoProductoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PedidoProducto.objects.filter(usuario=self.request.user)

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)