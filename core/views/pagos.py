from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..models import MetodoPago, BitacoraPago
from ..serializers import MetodoPagoSerializer, BitacoraPagoSerializer


class MetodoPagoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MetodoPago.objects.all()
    serializer_class = MetodoPagoSerializer
    permission_classes = [IsAuthenticated]


class BitacoraPagoViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = BitacoraPagoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return BitacoraPago.objects.filter(usuario=self.request.user)

    @action(detail=False, methods=['post'])
    def iniciar_pago_paypal(self, request):
        # Aquí iría la lógica para iniciar el pago con PayPal
        # Este es un ejemplo simplificado
        tipo = request.data.get('tipo')
        id = request.data.get('id')

        # Lógica para iniciar el pago...

        return Response({"message": "Pago iniciado"}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def confirmar_pago_paypal(self, request):
        # Aquí iría la lógica para confirmar el pago con PayPal
        # Este es un ejemplo simplificado
        paymentId = request.data.get('paymentId')
        PayerID = request.data.get('PayerID')

        # Lógica para confirmar el pago...

        return Response({"message": "Pago confirmado"}, status=status.HTTP_200_OK)