from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.urls import reverse
from paypalrestsdk import Payment
from ..models import Reserva, InscripcionCurso, PedidoProducto, MetodoPago

def iniciar_pago_paypal(request, tipo, id):
    if tipo == 'servicio':
        objeto = get_object_or_404(Reserva, id=id, usuario=request.user)
    elif tipo == 'curso':
        objeto = get_object_or_404(InscripcionCurso, id=id, usuario=request.user)
    elif tipo == 'producto':
        objeto = get_object_or_404(PedidoProducto, id=id, usuario=request.user)
    else:
        return redirect('error')

    metodo_pago = MetodoPago.objects.get(tipo='paypal')

    paypal_dict = {
        "intent": "sale",
        "payer": {"payment_method": "paypal"},
        "redirect_urls": {
            "return_url": request.build_absolute_uri(reverse('pago_completado')),
            "cancel_url": request.build_absolute_uri(reverse('pago_cancelado')),
        },
        "transactions": [{
            "amount": {
                "total": str(objeto.precio_total),
                "currency": "MXN",
            },
            "description": f"Pago por {tipo}: {objeto}",
        }]
    }

    payment = Payment(paypal_dict)
    if payment.create():
        objeto.paypal_order_id = payment.id
        objeto.save()
        for link in payment.links:
            if link.rel == "approval_url":
                return redirect(link.href)
    else:
        return redirect('error')

def pago_completado(request):
    paymentId = request.GET.get('paymentId')
    payment = Payment.find(paymentId)
    if payment.execute({"payer_id": request.GET.get('PayerID')}):
        # Buscar el objeto correspondiente y actualizar su estado
        for modelo in [Reserva, InscripcionCurso, PedidoProducto]:
            objeto = modelo.objects.filter(paypal_order_id=paymentId).first()
            if objeto:
                objeto.estado = 'pagado'
                objeto.save()
                metodo_pago = MetodoPago.objects.get(tipo='paypal')
                objeto.registrar_pago(
                    monto=payment.transactions[0].amount.total,
                    metodo_pago=metodo_pago,
                    estado='completado',
                    detalles=f"PayPal Transaction ID: {payment.id}"
                )
                return render(request, 'pago_exitoso.html')
    return redirect('error')

def pago_cancelado(request):
    return render(request, 'pago_cancelado.html')