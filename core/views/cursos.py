from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from ..models import Curso, InscripcionCurso
from ..serializers import CursoSerializer, InscripcionCursoSerializer

class CursoViewSet(viewsets.ModelViewSet):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

class InscripcionCursoViewSet(viewsets.ModelViewSet):
    serializer_class = InscripcionCursoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return InscripcionCurso.objects.filter(usuario=self.request.user)

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)